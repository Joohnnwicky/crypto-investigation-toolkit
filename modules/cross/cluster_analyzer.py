"""Address clustering module for multi-address association analysis"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

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
TIME_OVERLAP_THRESHOLD = 70    # D-07: minimum overlap percentage
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


def calculate_activity_window(address: str, tx_data: Dict) -> Dict:
    """Calculate activity time window for an address.

    Args:
        address: Target address
        tx_data: Transaction data dict

    Returns:
        Dict with first_ts, last_ts, duration_days
    """
    timestamps = []
    chain = tx_data.get('chain', 'unknown')

    if chain == 'tron':
        transfers = tx_data.get('trc20_transfers', [])
        for t in transfers:
            ts = t.get('block_timestamp', 0)
            if ts > 0:
                timestamps.append(ts)

    elif chain == 'eth':
        txs = tx_data.get('eth_transactions', [])
        for t in txs:
            ts = int(t.get('timeStamp', 0))
            if ts > 0:
                timestamps.append(ts)

    if not timestamps:
        return {'first_ts': 0, 'last_ts': 0, 'duration_days': 0}

    first_ts = min(timestamps)
    last_ts = max(timestamps)
    duration_days = (last_ts - first_ts) / (24 * 60 * 60 * 1000) if chain == 'tron' else (last_ts - first_ts) / (24 * 60 * 60)

    return {
        'first_ts': first_ts,
        'last_ts': last_ts,
        'duration_days': round(duration_days, 1)
    }


def calculate_time_overlap(window1: Dict, window2: Dict) -> int:
    """Calculate time window overlap percentage.

    Args:
        window1: First address activity window
        window2: Second address activity window

    Returns:
        Overlap percentage (0-100)
    """
    if window1.get('first_ts', 0) == 0 or window2.get('first_ts', 0) == 0:
        return 0

    # Normalize timestamps (handle different units)
    start1 = window1['first_ts']
    end1 = window1['last_ts']
    start2 = window2['first_ts']
    end2 = window2['last_ts']

    # Calculate overlap
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    if overlap_start >= overlap_end:
        return 0

    overlap_duration = overlap_end - overlap_start
    total_duration = max(end1 - start1, end2 - start2)

    if total_duration == 0:
        return 0

    overlap_pct = int((overlap_duration / total_duration) * 100)
    return min(100, max(0, overlap_pct))


def find_shared_deposit(addr1: str, addr2: str, address_data: Dict) -> Optional[str]:
    """Find shared deposit address used by both addresses.

    Args:
        addr1: First address
        addr2: Second address
        address_data: Dict with address transaction data

    Returns:
        Shared deposit address or None
    """
    # Get first funding sources for both
    tx1 = address_data.get(addr1, {})
    tx2 = address_data.get(addr2, {})

    source1 = find_first_funding_source(addr1, tx1.get('chain'), tx1)
    source2 = find_first_funding_source(addr2, tx2.get('chain'), tx2)

    if source1 and source2 and source1 == source2:
        return source1

    return None


def cluster_addresses_web(addresses: List[str], api_keys: Dict[str, str]) -> Dict[str, Any]:
    """Web interface for address clustering.

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
                # TRON: Use Tronscan API (free, no key required)
                account_info = get_account_info(addr)
                trc20_transfers = get_trc20_transfers(addr, limit=50)
                tx_data['account_info'] = account_info
                tx_data['trc20_transfers'] = trc20_transfers

            elif chain == 'eth':
                # ETH: Use Etherscan API (requires key)
                eth_txs = get_eth_transactions(addr, eth_key, limit=100)
                erc20_transfers = get_erc20_transfers(addr, eth_key, limit=100)
                tx_data['eth_transactions'] = eth_txs
                tx_data['erc20_transfers'] = erc20_transfers

            elif chain == 'btc':
                # BTC: Blockstream free API - limited address history
                # Note: Blockstream API requires tx_hash, not address lookup
                # For clustering, we'll mark BTC addresses as limited data
                tx_data['btc_transactions'] = []
                tx_data['limited_data'] = True

        except Exception as e:
            logger.warning(f"Failed to fetch data for {addr}: {e}")
            tx_data['error'] = str(e)

        address_data[addr] = tx_data

    # Apply clustering heuristics (D-05 to D-08)
    clusters = []
    checked = set()

    for addr1 in addresses:
        if addr1 in checked:
            continue

        cluster_addresses = [addr1]
        cluster_reasons = []
        cluster_details = {
            'shared_source': None,
            'mutual_transfers': [],
            'time_window': None,
            'shared_deposit': None
        }

        chain1 = address_chain_map[addr1]
        tx1 = address_data.get(addr1, {})

        # Calculate activity window for addr1
        window1 = calculate_activity_window(addr1, tx1)

        for addr2 in addresses:
            if addr2 == addr1 or addr2 in checked:
                continue

            chain2 = address_chain_map[addr2]

            # Skip cross-chain clustering (different chains)
            if chain1 != chain2:
                continue

            tx2 = address_data.get(addr2, {})
            window2 = calculate_activity_window(addr2, tx2)

            # D-05: First funding source match
            source1 = find_first_funding_source(addr1, chain1, tx1)
            source2 = find_first_funding_source(addr2, chain2, tx2)
            if source1 and source2 and source1 == source2:
                if addr2 not in cluster_addresses:
                    cluster_addresses.append(addr2)
                cluster_reasons.append(f"首次资金来源相同: {source1}")
                cluster_details['shared_source'] = source1

            # D-06: Frequent mutual transfers
            mutual = check_mutual_transfers(addr1, addr2, address_data)
            total_mutual = sum(m.get('count', 0) for m in mutual)
            if total_mutual >= MUTUAL_TRANSFER_THRESHOLD:
                if addr2 not in cluster_addresses:
                    cluster_addresses.append(addr2)
                cluster_reasons.append(f"频繁互转账: {total_mutual}次")
                cluster_details['mutual_transfers'].extend(mutual)

            # D-07: Time window overlap
            overlap = calculate_time_overlap(window1, window2)
            if overlap >= TIME_OVERLAP_THRESHOLD:
                if addr2 not in cluster_addresses:
                    cluster_addresses.append(addr2)
                cluster_reasons.append(f"时间窗口关联: {overlap}%重叠")
                cluster_details['time_window'] = {'overlap_pct': overlap}

            # D-08: Shared deposit address
            shared_deposit = find_shared_deposit(addr1, addr2, address_data)
            if shared_deposit:
                if addr2 not in cluster_addresses:
                    cluster_addresses.append(addr2)
                cluster_reasons.append(f"共享存款地址: {shared_deposit}")
                cluster_details['shared_deposit'] = shared_deposit

        # Only create cluster if more than one address found
        if len(cluster_addresses) > 1:
            # Calculate total transactions for cluster
            total_txs = 0
            for addr in cluster_addresses:
                tx = address_data.get(addr, {})
                if chain1 == 'tron':
                    total_txs += len(tx.get('trc20_transfers', []))
                elif chain1 == 'eth':
                    total_txs += len(tx.get('eth_transactions', []))

            cluster = {
                'cluster_id': len(clusters) + 1,
                'addresses': cluster_addresses,
                'chain_types': [address_chain_map[a] for a in cluster_addresses],
                'reasons': cluster_reasons,
                'shared_source': cluster_details['shared_source'],
                'mutual_transfers': cluster_details['mutual_transfers'],
                'time_window': cluster_details['time_window'],
                'shared_deposit': cluster_details['shared_deposit'],
                'stats': {
                    'total_transactions': total_txs,
                    'total_volume': '计算需更详细分析'
                }
            }
            clusters.append(cluster)
            checked.update(cluster_addresses)

    # Unassociated addresses (D-11)
    unassociated = [a for a in addresses if a not in checked]

    return {
        'success': True,
        'addresses': addresses,
        'clusters': clusters,
        'unassociated': unassociated
    }