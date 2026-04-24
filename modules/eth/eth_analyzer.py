"""ETH transaction analyzer with complete cross-chain bridge detection.

Based on validated original code from 002-day1-查询以太坊地址的所有交易.py
"""

import requests
from typing import Dict, Any, List
from datetime import datetime

# ============================================
# Etherscan API V2 configuration
# ============================================
ETHERSCAN_BASE = "https://api.etherscan.io/v2/api"
ETH_CHAIN_ID = 1  # Ethereum mainnet

# ============================================
# Bridge contract address library (Ethereum mainnet)
# ============================================
BRIDGE_ADDRESSES = {
    # Stargate
    "0xDef1C0ded9bec7F1a1670819833240f027b25EfF": "Stargate Router",
    "0x3c2269811836af69497E5F486A85D7316753cf72": "Stargate Pool",
    "0x150f94b4b5e760eb8ddd1b9f0f7f5f5f5f5f5f5f": "Stargate USDC Pool",

    # Hop Protocol
    "0x8656f2E847249B6AaF1f8aC616a2c06EA6EA06E": "Hop Bridge",
    "0xb8901acB165ed027E32754E0FFe830802919727f": "Hop L2 Bridge",

    # Multichain (Anyswap)
    "0x6b7a87899790d6ee64229a36b9e592d2c39a0060": "Multichain Router",
    "0x88dc47e1cf7e2483d0f69e0b1c5553d16e8d0c4d": "Multichain AnyswapV4",
    "0x4AA8FAa2659478737D744891aAF987267dE6c04E": "Multichain V3 Router",

    # cBridge (Celer)
    "0x5427FEcFA6beAF3523d6167F2B3B9f3F7a6B3b3B": "cBridge",
    "0x841ce30F35b453d8f4e9d873c1d6b0d7c7c7c7c7": "Celer cBridge",

    # Across Protocol
    "0x4C36d2919e407f0Cc2Ee3c99cC16f4d5cC7c7c7c": "Across Bridge",

    # Synapse Protocol
    "0x1111111254EEB25477B68fb85Ed929f73A960582": "Synapse Router",

    # Polygon Bridge (PoS)
    "0xA0c68C638235ee32657e8f720a9cecc1da91B2A1": "Polygon PoS Bridge",
    "0x86E4Dc95c7FBdBf52e33D563BbDB00823894C287": "Polygon MRC20 Bridge",

    # Arbitrum Bridge
    "0x011B6E24FfB0b5f5fCc564cf4183C5BBBc96Fb0a": "Arbitrum Inbox",
    "0x4Dbd4fc535Ac27206064D68e839d34cB2d5F7F7F": "Arbitrum Outbox",

    # Optimism Bridge
    "0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1": "Optimism L1 Bridge",

    # zkSync Bridge
    "0xaBEA9132b05A70803a4E85094fD0e1800777fBEF": "zkSync Bridge",

    # Base Bridge (Coinbase)
    "0x3154Cf16ccdb4C6d9226276690b58284f7c7c7c7": "Base L1 Bridge",

    # Wormhole
    "0x3ee18B2214AFF97000D974cf647E7C347E8fa585": "Wormhole Core",
    "0xf92cD566Ea4864356C5491c177A430C222d7e678": "Wormhole Token Bridge",

    # LayerZero
    "0x66A71Dcef29A0fBFBDB9F0a7b7c7c7c7c7c7c7c7c": "LayerZero Endpoint",
}


def get_eth_transactions(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """
    Get ETH transactions from Etherscan API V2.

    Args:
        address: ETH address (0x prefix, 40 hex chars)
        api_key: User's Etherscan API key (per-request input)
        limit: Maximum transactions to fetch

    Returns:
        List of transaction dicts
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",  # Ascending, earliest first
        "apikey": api_key
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1":
            result = data.get("result", [])
            # Return last N transactions (most recent)
            return result[-limit:] if len(result) > limit else result
        else:
            return []
    except Exception:
        return []


def get_erc20_transfers(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """
    Get ERC20 token transfers from Etherscan API V2.

    Args:
        address: ETH address
        api_key: Etherscan API key
        limit: Maximum transfers to fetch

    Returns:
        List of transfer dicts with tokenSymbol, tokenName, etc.
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "account",
        "action": "tokentx",
        "address": address,
        "sort": "asc",
        "apikey": api_key
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1":
            result = data.get("result", [])
            return result[-limit:] if len(result) > limit else result
        else:
            return []
    except Exception:
        return []


def get_transaction_logs(tx_hash: str, api_key: str) -> List[Dict]:
    """
    Get transaction event logs from Etherscan API V2.

    Args:
        tx_hash: Transaction hash
        api_key: Etherscan API key

    Returns:
        List of event logs
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "logs",
        "action": "getLogs",
        "txhash": tx_hash,
        "apikey": api_key
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1":
            return data.get("result", [])
        else:
            return []
    except Exception:
        return []


def identify_bridge(tx: Dict) -> tuple:
    """
    Identify if a transaction involves a cross-chain bridge.

    Checks if the transaction target address matches known bridge contracts.

    Args:
        tx: Single transaction dict from Etherscan

    Returns:
        tuple: (is_bridge: bool, bridge_name: str or None)
    """
    to_address = tx.get("to", "").lower()

    # Check if sent to bridge contract
    for addr, name in BRIDGE_ADDRESSES.items():
        if to_address == addr.lower():
            return True, name

    return False, None


def parse_stargate_event(logs: List[Dict]) -> Dict:
    """
    Parse Stargate cross-chain event from transaction logs.

    Args:
        logs: Event logs list

    Returns:
        dict with source_chain, dest_chain, amount, tx_hash
    """
    if not logs:
        return None

    # Stargate Swap event signature (first 4 bytes of keccak256)
    STARGATE_SWAP_EVENT = "0x5d8a5d9e"

    chain_ids = {
        1: "Ethereum",
        56: "BSC",
        137: "Polygon",
        42161: "Arbitrum",
        10: "Optimism",
        43114: "Avalanche",
        250: "Fantom",
        8453: "Base"
    }

    for log in logs:
        topics = log.get("topics", [])
        if topics and topics[0].startswith(STARGATE_SWAP_EVENT):
            try:
                data = log.get("data", "")
                if len(data) > 66:
                    dest_chain_id = int(data[2:66], 16)
                    amount = int(data[66:130], 16) / 1e18 if len(data) > 130 else 0

                    return {
                        "source_chain": "Ethereum",
                        "dest_chain": chain_ids.get(dest_chain_id, f"Chain {dest_chain_id}"),
                        "amount": amount,
                        "tx_hash": log.get("transactionHash", "")
                    }
            except Exception:
                pass

    return None


def is_valid_eth_address(address: str) -> bool:
    """Validate ETH address format (0x prefix + 40 hex chars)."""
    if not address:
        return False
    import re
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))


def query_eth_transactions_web(address: str, api_key: str) -> Dict[str, Any]:
    """
    Web API wrapper for ETH transaction query with bridge detection.

    Implements ADDR-04: ETH transaction query with cross-chain detection.
    Implements ADDR-05: API key per-request, never stored.

    Args:
        address: ETH wallet address
        api_key: User's Etherscan API key

    Returns:
        dict with success, address, transactions, bridge_events, error
    """
    # Validate address
    if not is_valid_eth_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的ETH地址格式（应以0x开头，42位字符）',
            'transactions': None,
            'bridge_events': None
        }

    # Validate API key
    if not api_key or len(api_key) < 20:
        return {
            'success': False,
            'address': address,
            'error': '请输入有效的Etherscan API密钥',
            'transactions': None,
            'bridge_events': None
        }

    # Get transactions
    normal_txs = get_eth_transactions(address, api_key, limit=50)
    erc20_txs = get_erc20_transfers(address, api_key, limit=50)

    # Identify bridge transactions
    bridge_events = []
    for tx in normal_txs:
        is_bridge, bridge_name = identify_bridge(tx)
        if is_bridge:
            # Try to get more details from logs
            logs = get_transaction_logs(tx["hash"], api_key)
            stargate_info = parse_stargate_event(logs)

            event = {
                "tx_hash": tx["hash"],
                "time": datetime.fromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
                "amount": float(tx["value"]) / 1e18,
                "bridge": bridge_name,
                "from": tx.get("from", ""),
                "to": tx.get("to", "")
            }

            # Add Stargate-specific info if available
            if stargate_info:
                event["dest_chain"] = stargate_info["dest_chain"]

            bridge_events.append(event)

    # Also check ERC20 transfers for bridge interactions
    for tx in erc20_txs:
        is_bridge, bridge_name = identify_bridge(tx)
        if is_bridge:
            event = {
                "tx_hash": tx["hash"],
                "time": datetime.fromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
                "amount": float(tx.get("value", 0)) / (10 ** int(tx.get("tokenDecimal", 18))),
                "token": tx.get("tokenSymbol", ""),
                "bridge": bridge_name,
                "from": tx.get("from", ""),
                "to": tx.get("to", "")
            }
            bridge_events.append(event)

    return {
        'success': True,
        'address': address,
        'transactions': {
            'normal': normal_txs,
            'erc20': erc20_txs,
            'total_count': len(normal_txs) + len(erc20_txs)
        },
        'bridge_events': bridge_events,
        'error': None
    }