"""Stargate bridge detection using Known Contract Scan method.

Implements D-05: Check if ETH transaction interacts with known Stargate contracts.
Contract addresses verified from LayerZero/Stargate official documentation.
"""

from typing import Dict, List

# Stargate contract addresses on Ethereum mainnet
# Source: https://stargateprotocol.gitbook.io/stargate
STARGATE_CONTRACTS = {
    'router': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
    'router_eth': '0x150f94B44927F078737562f0fcF3C95c01Cc2376',
    'bridge': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
    'factory': '0x06D538690AF257Da524f25D0CD52fD85b1c2173E',
    'pools': [
        '0x101816545F6bd2b1076434B54383a1E633390A2E',  # ETH pool
        '0xdf0770dF86a8034b3EFEf0A1Bb3c889B8332FF56',  # USDC pool
        '0x38EA452219524Bb87e18dE1C24D3bB59510BD783',  # USDT pool
    ]
}

def detect_stargate_bridge(transactions: List[Dict]) -> List[Dict]:
    """Scan transactions for Stargate bridge interactions using Known Contract Scan.

    Implements D-05: Check if transaction 'to' address matches known Stargate contracts.

    Args:
        transactions: List of transaction dicts from Etherscan API
                      Each dict should have keys: hash, to, from, value, timeStamp

    Returns:
        list of bridge event dicts with keys:
            - tx_hash: Transaction hash
            - contract_type: Type of Stargate contract (router, pool, etc.)
            - timestamp: Transaction timestamp
            - from_address: Sender address
            - to_address: Stargate contract address
            - value: Transaction value in Wei
        Empty list if no Stargate interactions found

    Note:
        Destination chain extraction is deferred (RESEARCH.md Open Question 1).
        This implementation shows contract_type only, not destination chain.
    """
    bridge_events = []

    if not transactions:
        return bridge_events

    # Build lowercase address lookup for comparison
    router_lower = STARGATE_CONTRACTS['router'].lower()
    router_eth_lower = STARGATE_CONTRACTS['router_eth'].lower()
    bridge_lower = STARGATE_CONTRACTS['bridge'].lower()
    factory_lower = STARGATE_CONTRACTS['factory'].lower()
    pools_lower = [addr.lower() for addr in STARGATE_CONTRACTS['pools']]

    for tx in transactions:
        to_address = tx.get('to', '')

        if not to_address:
            continue

        to_lower = to_address.lower()

        # Check router contracts (main routing interface)
        if to_lower == router_lower:
            bridge_events.append({
                'tx_hash': tx.get('hash', ''),
                'contract_type': 'router',
                'timestamp': tx.get('timeStamp', ''),
                'from_address': tx.get('from', ''),
                'to_address': to_address,
                'value': tx.get('value', '0')
            })
            continue

        # Check router_eth contract (native ETH swaps)
        if to_lower == router_eth_lower:
            bridge_events.append({
                'tx_hash': tx.get('hash', ''),
                'contract_type': 'router_eth',
                'timestamp': tx.get('timeStamp', ''),
                'from_address': tx.get('from', ''),
                'to_address': to_address,
                'value': tx.get('value', '0')
            })
            continue

        # Check bridge contract (LayerZero messaging)
        if to_lower == bridge_lower:
            bridge_events.append({
                'tx_hash': tx.get('hash', ''),
                'contract_type': 'bridge',
                'timestamp': tx.get('timeStamp', ''),
                'from_address': tx.get('from', ''),
                'to_address': to_address,
                'value': tx.get('value', '0')
            })
            continue

        # Check factory contract
        if to_lower == factory_lower:
            bridge_events.append({
                'tx_hash': tx.get('hash', ''),
                'contract_type': 'factory',
                'timestamp': tx.get('timeStamp', ''),
                'from_address': tx.get('from', ''),
                'to_address': to_address,
                'value': tx.get('value', '0')
            })
            continue

        # Check pool contracts (liquidity pools)
        for i, pool_addr in enumerate(pools_lower):
            if to_lower == pool_addr:
                # Determine pool type based on index
                pool_types = ['pool_eth', 'pool_usdc', 'pool_usdt']
                pool_type = pool_types[i] if i < len(pool_types) else 'pool'

                bridge_events.append({
                    'tx_hash': tx.get('hash', ''),
                    'contract_type': pool_type,
                    'timestamp': tx.get('timeStamp', ''),
                    'from_address': tx.get('from', ''),
                    'to_address': to_address,
                    'value': tx.get('value', '0')
                })
                break

    return bridge_events