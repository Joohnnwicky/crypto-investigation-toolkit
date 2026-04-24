"""BTC transaction analyzer module with Blockstream API integration"""

import logging
import re
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Blockstream API URL (per D-02, no API key required)
BLOCKSTREAM_API_URL = "https://blockstream.info/api/tx/"
BLOCKCHAIN_INFO_URL = "https://blockchain.info/rawtx/"  # Fallback

# Request timeout
DEFAULT_TIMEOUT = 10


def validate_tx_hash(tx_hash: str) -> bool:
    """Validate BTC transaction hash format.

    Args:
        tx_hash: Transaction hash string

    Returns:
        True if valid (64 hex chars), False otherwise
    """
    if not tx_hash:
        return False
    return bool(re.match(r'^[a-fA-F0-9]{64}$', tx_hash))


def identify_address_type(address: str) -> Dict[str, Any]:
    """Identify BTC address type.

    Args:
        address: BTC address string

    Returns:
        Dict with address, type, format, features, wallet_hint
    """
    result = {
        "address": address,
        "type": None,
        "format": None,
        "features": None,
        "wallet_hint": None
    }

    # P2PKH: Legacy address starting with 1
    if re.match(r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        result["type"] = "P2PKH"
        result["format"] = "Legacy (Legacy Address)"
        result["features"] = "最早期格式，仅支持单签名，交易费用较高"
        result["wallet_hint"] = "可能是较老的钱包或冷钱包"

    # P2SH: Script hash address starting with 3
    elif re.match(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        result["type"] = "P2SH"
        result["format"] = "Pay to Script Hash"
        result["features"] = "支持MultiSig、闪电网络、隔离见证兼容"
        result["wallet_hint"] = "可能是多重签名钱包、交易所热钱包"

    # P2WPKH: Native SegWit bc1q...
    elif re.match(r'^bc1q[ac-hj-np-z02-9]{39,59}$', address.lower()):
        result["type"] = "P2WPKH"
        result["format"] = "Native SegWit (原生隔离见证)"
        result["features"] = "费用较低，主流新钱包默认格式"
        result["wallet_hint"] = "现代软件钱包（Coinbase、Blockstream Green等）"

    # P2TR: Taproot bc1p...
    elif re.match(r'^bc1p[ac-hj-np-z02-9]{58}$', address.lower()):
        result["type"] = "P2TR"
        result["format"] = "Taproot (2021年启用)"
        result["features"] = "隐私性最强，费用最低，支持复杂脚本"
        result["wallet_hint"] = "最新钱包，支持Taproot的硬件/软件钱包"

    else:
        result["type"] = "Unknown"
        result["format"] = "无法识别"
        result["features"] = "可能是测试网地址或格式错误"

    return result


def fetch_transaction(tx_hash: str) -> Optional[Dict]:
    """Fetch BTC transaction from Blockstream API with fallback.

    Args:
        tx_hash: Transaction hash

    Returns:
        Transaction data dict or None
    """
    # Try Blockstream first
    try:
        response = requests.get(
            f"{BLOCKSTREAM_API_URL}{tx_hash}",
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.warning(f"Blockstream API failed: {e}")

    # Fallback to Blockchain.info
    try:
        response = requests.get(
            f"{BLOCKCHAIN_INFO_URL}{tx_hash}",
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Blockchain.info API failed: {e}")

    return None


def parse_transaction(tx_data: Dict) -> Dict:
    """Parse Blockstream API response into structured format.

    Args:
        tx_data: Raw API response

    Returns:
        Parsed transaction dict
    """
    result = {
        "txid": tx_data.get("txid", ""),
        "version": tx_data.get("version", 1),
        "size": tx_data.get("size", 0),
        "weight": tx_data.get("weight", 0),
        "fee": tx_data.get("fee", 0),  # satoshis
        "block_height": tx_data.get("status", {}).get("block_height", 0),
        "block_time": tx_data.get("status", {}).get("block_time", 0),
        "confirmed": tx_data.get("status", {}).get("confirmed", False),
        "vin": [],
        "vout": []
    }

    # Parse inputs (vin)
    for vin in tx_data.get("vin", []):
        result["vin"].append({
            "txid": vin.get("txid", ""),
            "vout": vin.get("vout", 0),
            "scriptsig": vin.get("scriptsig", ""),
            "sequence": vin.get("sequence", 0),
            "is_coinbase": vin.get("is_coinbase", False)
        })

    # Parse outputs (vout) with address type identification
    for vout in tx_data.get("vout", []):
        # Blockstream API: scriptpubkey is hex string, address is in scriptpubkey_address
        address = vout.get("scriptpubkey_address", "")
        address_info = identify_address_type(address) if address else None

        result["vout"].append({
            "value": vout.get("value", 0),  # satoshis
            "n": vout.get("n", 0),
            "address": address,
            "address_type": address_info.get("type") if address_info else None,
            "wallet_hint": address_info.get("wallet_hint") if address_info else None
        })

    return result


def calculate_fee_details(tx_data: Dict) -> Dict:
    """Calculate fee in BTC and fee rate.

    Args:
        tx_data: Transaction data

    Returns:
        Dict with fee_btc, fee_satoshis, fee_rate_sat_vb, tx_size_vb
    """
    fee_satoshis = tx_data.get("fee", 0)
    weight = tx_data.get("weight", 0)

    fee_btc = fee_satoshis / 10**8
    tx_size_vb = weight / 4 if weight > 0 else tx_data.get("size", 0)
    fee_rate_sat_vb = fee_satoshis / tx_size_vb if tx_size_vb > 0 else 0

    return {
        "fee_btc": fee_btc,
        "fee_satoshis": fee_satoshis,
        "fee_rate_sat_vb": round(fee_rate_sat_vb, 2),
        "tx_size_vb": tx_size_vb
    }


def generate_transaction_summary(parsed: Dict, fee_details: Dict) -> str:
    """Generate ASCII summary diagram.

    Args:
        parsed: Parsed transaction data
        fee_details: Fee calculation details

    Returns:
        ASCII diagram string
    """
    vin_count = len(parsed.get("vin", []))
    vout_count = len(parsed.get("vout", []))
    txid_short = parsed.get("txid", "")[:16]

    summary = f"""
┌─────────────────────────────────────────────────────────────┐
│  BTC交易解析                                                 │
├─────────────────────────────────────────────────────────────┤
│  交易ID: {txid_short}...                                     │
│  输入数: {vin_count}                                         │
│  输出数: {vout_count}                                        │
│  手续费: {fee_details['fee_btc']} BTC ({fee_details['fee_rate_sat_vb']} sat/vB) │
│  状态: {'已确认' if parsed.get('confirmed') else '未确认'}   │
│                                                              │
│  地址类型分析:                                                │
└─────────────────────────────────────────────────────────────┘
"""
    return summary


def analyze_btc_transaction_web(tx_hash: str) -> Dict[str, Any]:
    """Web interface for BTC transaction analysis.

    Args:
        tx_hash: Bitcoin transaction hash (64 hex chars)

    Returns:
        Dict with success, tx_hash, transaction, summary
    """
    # Validate tx_hash format
    if not validate_tx_hash(tx_hash):
        return {
            "success": False,
            "error": "无效的交易哈希格式（需要64位十六进制）",
            "tx_hash": tx_hash
        }

    tx_data = fetch_transaction(tx_hash)
    if not tx_data:
        return {
            "success": False,
            "error": "无法获取交易数据（API请求失败）",
            "tx_hash": tx_hash
        }

    parsed = parse_transaction(tx_data)
    fee_details = calculate_fee_details(tx_data)

    # Format block time
    block_time = parsed.get("block_time", 0)
    block_time_str = datetime.fromtimestamp(block_time).strftime("%Y-%m-%d %H:%M:%S") if block_time > 0 else "未确认"

    # Add formatted time to parsed data
    parsed["block_time_formatted"] = block_time_str
    parsed["fee"] = fee_details

    return {
        "success": True,
        "tx_hash": tx_hash,
        "transaction": parsed,
        "summary": generate_transaction_summary(parsed, fee_details)
    }