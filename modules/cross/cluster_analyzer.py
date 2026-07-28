"""Address clustering module for multi-address association analysis"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from .chain_detector import detect_chain_type, get_chain_requirements
from modules.core.api_client import (
    get_account_info,
    get_trc20_transfers,
    get_eth_transactions,
    get_erc20_transfers
)
from modules.trace.btc_analyzer import fetch_transaction, identify_address_type

logger = logging.getLogger(__name__)

# Clustering thresholds (per RESEARCH.md recommendation)
MUTUAL_TRANSFER_THRESHOLD = 2  # D-06: minimum mutual transfers
DEFAULT_TIMEOUT = 10


def find_first_funding_source(address: str, chain: str, tx_data: Dict) -> Optional[str]:
    """Find first incoming transaction source address.

    Args:
        address: Target address
        chain: Chain type ('tron', 'eth', 'btc')
        tx_data: Transaction data dict

    Returns:
        First funding source address or None
    """
    if chain == 'tron':
        # Check TRC20 transfers for first incoming
        transfers = tx_data.get('trc20_transfers', [])
        incoming = [t for t in transfers if t.get('to_address') == address]
        if incoming:
            # Sort by timestamp, get earliest
            sorted_incoming = sorted(incoming, key=lambda x: x.get('block_timestamp', 0))
            return sorted_incoming[0].get('from_address')

    elif chain == 'eth':
        # Check ETH transactions for first incoming
        txs = tx_data.get('eth_transactions', [])
        incoming = [t for t in txs if t.get('to', '').lower() == address.lower()]
        if incoming:
            # Sort by timestamp, get earliest
            sorted_incoming = sorted(incoming, key=lambda x: int(x.get('timeStamp', 0)))
            return sorted_incoming[0].get('from')

    elif chain == 'btc':
        # BTC requires transaction hash lookup, not address history directly
        # Return None for BTC as we need individual tx lookups
        pass

    return None


def check_mutual_transfers(addr1: str, addr2: str, address_data: Dict) -> List[Dict]:
    """Check mutual transfers between two addresses.

    Args:
        addr1: First address
        addr2: Second address
        address_data: Dict with address transaction data

    Returns:
        List of mutual transfer dicts with direction and count
    """
    mutual = []

    # Get transactions for both addresses
    tx1 = address_data.get(addr1, {})
    tx2 = address_data.get(addr2, {})

    chain1 = tx1.get('chain', 'unknown')
    chain2 = tx2.get('chain', 'unknown')

    # Only check if same chain
    if chain1 != chain2:
        return mutual

    if chain1 == 'tron':
        # Check TRC20 transfers
        transfers1 = tx1.get('trc20_transfers', [])
        transfers2 = tx2.get('trc20_transfers', [])

        # addr1 -> addr2
        count_1_to_2 = len([t for t in transfers1 if t.get('to_address') == addr2])
        # addr2 -> addr1
        count_2_to_1 = len([t for t in transfers2 if t.get('to_address') == addr1])

        if count_1_to_2 > 0:
            mutual.append({'from': addr1, 'to': addr2, 'count': count_1_to_2})
        if count_2_to_1 > 0:
            mutual.append({'from': addr2, 'to': addr1, 'count': count_2_to_1})

    elif chain1 == 'eth':
        # Check ETH transactions
        eth_txs1 = tx1.get('eth_transactions', [])
        eth_txs2 = tx2.get('eth_transactions', [])

        # addr1 -> addr2
        count_1_to_2 = len([t for t in eth_txs1 if t.get('to', '').lower() == addr2.lower()])
        # addr2 -> addr1
        count_2_to_1 = len([t for t in eth_txs2 if t.get('to', '').lower() == addr1.lower()])

        if count_1_to_2 > 0:
            mutual.append({'from': addr1, 'to': addr2, 'count': count_1_to_2})
        if count_2_to_1 > 0:
            mutual.append({'from': addr2, 'to': addr1, 'count': count_2_to_1})

    return mutual


def cluster_addresses_web(addresses: List[str], api_keys: Dict[str, str]) -> Dict[str, Any]:
    """Web interface for address clustering.

    Clustering is conservative and evidence-based. Two signals are used:
      - Mutual transfers between two addresses (>= threshold).
      - Co-funding: both addresses' first funding source is itself one of
        the input addresses under investigation (a suspect funder).

    Removed signals (false-positive prone):
      - "Same first funding source": most addresses are first funded by the
        same exchange hot wallet, which would cluster unrelated addresses.
      - "Activity time-window overlap": two unrelated addresses active in
        the same period is noise, not a clustering signal.

    BTC is not clustered: co-spend (common-input) heuristics are not
    implemented, and Blockstream's free API has no address history endpoint.
    BTC addresses are reported as unassociated.

    Args:
        addresses: List of wallet addresses (max 10 per D-01)
        api_keys: Dict with 'eth_key' (optional for TRON/BTC)

    Returns:
        Dict with success, addresses, clusters, unassociated
    """
    # Validate address count (D-01)
    if not addresses:
        return {'success': False, 'error': '请输入至少一个地址'}

    if len(addresses) > 10:
        return {'success': False, 'error': '地址数量超过10个限制'}

    # Clean addresses (strip whitespace)
    addresses = [addr.strip() for addr in addresses if addr.strip()]

    # Detect chain types and validate
    address_chain_map = {}
    needs_eth_key = False

    for addr in addresses:
        chain = detect_chain_type(addr)
        if chain == 'unknown':
            return {'success': False, 'error': f'无法识别地址链类型: {addr}'}
        address_chain_map[addr] = chain
        if chain == 'eth':
            needs_eth_key = True

    # Validate API keys (D-03)
    eth_key = api_keys.get('eth_key', '').strip()
    if needs_eth_key and not eth_key:
        return {'success': False, 'error': 'ETH地址需要Etherscan API密钥'}

    # Fetch transaction data for each address
    address_data = {}

    for addr in addresses:
        chain = address_chain_map[addr]
        tx_data = {'chain': chain, 'transactions': []}

        try:
            if chain == 'tron':
                account_info = get_account_info(addr)
                trc20_transfers = get_trc20_transfers(addr, limit=50)
                tx_data['account_info'] = account_info
                tx_data['trc20_transfers'] = trc20_transfers

            elif chain == 'eth':
                eth_txs = get_eth_transactions(addr, eth_key, limit=100)
                erc20_transfers = get_erc20_transfers(addr, eth_key, limit=100)
                tx_data['eth_transactions'] = eth_txs
                tx_data['erc20_transfers'] = erc20_transfers

            elif chain == 'btc':
                # Blockstream free API has no address-history endpoint usable
                # for clustering (co-spend not implemented). Mark limited.
                tx_data['btc_transactions'] = []
                tx_data['limited_data'] = True

        except Exception as e:
            logger.warning(f"Failed to fetch data for {addr}: {e}")
            tx_data['error'] = str(e)

        address_data[addr] = tx_data

    # ---- Union-Find over input addresses ----
    parent = {a: a for a in addresses}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    address_set = set(addresses)
    # Per-pair evidence: (a1, a2) -> {'reasons': [...], 'mutual': [...]}
    pair_evidence: Dict[tuple, Dict[str, Any]] = {}

    for i, addr1 in enumerate(addresses):
        chain1 = address_chain_map[addr1]
        if chain1 == 'btc':
            continue  # BTC not clustered
        tx1 = address_data.get(addr1, {})
        funder1 = find_first_funding_source(addr1, chain1, tx1)

        for addr2 in addresses[i + 1:]:
            chain2 = address_chain_map[addr2]
            if chain2 != chain1:
                continue  # cross-chain not comparable

            tx2 = address_data.get(addr2, {})
            reasons: List[str] = []

            # D-06: frequent mutual transfers
            mutual = check_mutual_transfers(addr1, addr2, address_data)
            total_mutual = sum(m.get('count', 0) for m in mutual)
            if total_mutual >= MUTUAL_TRANSFER_THRESHOLD:
                union(addr1, addr2)
                reasons.append(f"频繁互转账: {total_mutual}次")

            # Co-funder: shared first funding source that is itself in the
            # input set. A shared arbitrary exchange funder is NOT a signal.
            funder2 = find_first_funding_source(addr2, chain2, tx2)
            if (funder1 and funder2 and funder1 == funder2
                    and funder1 in address_set):
                union(addr1, addr2)
                reasons.append(f"被同一调查地址资助: {funder1}")

            if reasons:
                pair_evidence[(addr1, addr2)] = {'reasons': reasons, 'mutual': mutual}

    # ---- Build clusters from connected components ----
    components: Dict[str, List[str]] = defaultdict(list)
    for a in addresses:
        components[find(a)].append(a)

    clusters = []
    for comp_addrs in components.values():
        if len(comp_addrs) <= 1:
            continue

        chain_types = [address_chain_map[a] for a in comp_addrs]
        primary_chain = chain_types[0]

        # Aggregate reasons + mutual transfers across all in-component pairs
        reasons: List[str] = []
        mutual_transfers: List[Dict] = []
        shared_funder = None
        funder_seen = set()

        for idx, a1 in enumerate(comp_addrs):
            f1 = find_first_funding_source(a1, address_chain_map[a1], address_data.get(a1, {}))
            if f1:
                funder_seen.add(f1)
            for a2 in comp_addrs[idx + 1:]:
                ev = pair_evidence.get((a1, a2)) or pair_evidence.get((a2, a1))
                if ev:
                    reasons.extend(ev['reasons'])
                    mutual_transfers.extend(ev['mutual'])

        # Shared funder only if exactly one distinct funder and it is in the set
        if len(funder_seen) == 1:
            sole_funder = next(iter(funder_seen))
            if sole_funder in address_set:
                shared_funder = sole_funder

        # Total transactions (TRC20 / ETH record count)
        total_txs = 0
        for addr in comp_addrs:
            tx = address_data.get(addr, {})
            if primary_chain == 'tron':
                total_txs += len(tx.get('trc20_transfers', []))
            elif primary_chain == 'eth':
                total_txs += len(tx.get('eth_transactions', []))

        cluster = {
            'cluster_id': len(clusters) + 1,
            'addresses': comp_addrs,
            'chain_types': chain_types,
            'reasons': reasons,
            'shared_source': shared_funder,
            'mutual_transfers': mutual_transfers,
            'time_window': None,  # removed (noise); key retained for API compat
            'shared_deposit': shared_funder,
            'stats': {
                'total_transactions': total_txs,
                'total_volume': '计算需更详细分析'
            }
        }
        clusters.append(cluster)

    # Unassociated addresses (singletons + BTC)
    associated = set()
    for c in clusters:
        associated.update(c['addresses'])
    unassociated = [a for a in addresses if a not in associated]

    return {
        'success': True,
        'addresses': addresses,
        'clusters': clusters,
        'unassociated': unassociated
    }