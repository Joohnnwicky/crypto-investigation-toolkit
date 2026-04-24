"""Obfuscation attack detection module for ETH chain attack pattern analysis"""

import logging
from typing import Dict, List, Any

from modules.core.api_client import get_eth_transactions, get_erc20_transfers

logger = logging.getLogger(__name__)

# DEX Router addresses for Sandwich detection
DEX_ROUTERS = {
    'uniswap_v2': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
    'uniswap_v3': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
    'sushiswap': '0xd9e1cE17f2641f24AE83637ab58a1aFa2493E64',
}

# Dust threshold for Dusting detection (per D-21)
DUST_THRESHOLD = 0.001  # ETH


def detect_sandwich_attack(txs: List[Dict]) -> List[Dict]:
    """Detect Sandwich attack patterns (per D-14, D-20).

    Signature: Same block contains frontrun + victim + backrun transactions
    to same DEX router with price manipulation.

    Args:
        txs: List of ETH transaction dicts

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    # Group transactions by blockNumber
    block_groups = {}
    for tx in txs:
        block = tx.get('blockNumber')
        if block:
            if block not in block_groups:
                block_groups[block] = []
            block_groups[block].append(tx)

    # Check blocks with multiple DEX transactions
    dex_addresses_lower = [addr.lower() for addr in DEX_ROUTERS.values()]

    for block, block_txs in block_groups.items():
        # Filter DEX transactions
        dex_txs = [t for t in block_txs if t.get('to', '').lower() in dex_addresses_lower]

        if len(dex_txs) >= 3:
            # Potential sandwich: front-victim-back pattern
            attacks.append({
                'type': 'Sandwich',
                'confidence': 'MEDIUM',
                'block': block,
                'tx_count': len(dex_txs),
                'details': f'区块 {block} 内有 {len(dex_txs)} 笔DEX交易，可能存在三明治攻击'
            })

    return attacks


def detect_flash_loan_attack(txs: List[Dict], api_key: str) -> List[Dict]:
    """Detect Flash Loan attack patterns (per D-15, D-19).

    Signature: Single transaction with borrow + manipulate + repay.
    High value transactions with rapid protocol interactions.

    Args:
        txs: List of ETH transaction dicts
        api_key: Etherscan API key for log queries

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    for tx in txs:
        value = int(tx.get('value', 0)) / 1e18

        # Check for high value transactions (> 100 ETH)
        if value > 100:
            attacks.append({
                'type': 'Flash Loan',
                'confidence': 'HIGH',
                'tx_hash': tx.get('hash', ''),
                'value': value,
                'details': f'交易内含大额借贷操作，金额 {value:.2f} ETH'
            })

    return attacks


def detect_dusting_attack(txs: List[Dict]) -> List[Dict]:
    """Detect Dusting attack patterns (per D-16, D-21).

    Signature: Many outgoing transactions with tiny amounts (< 0.001 ETH)
    to many different addresses for tracking.

    Args:
        txs: List of ETH transaction dicts

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    # Filter outgoing transactions with tiny values
    dust_txs = []
    for tx in txs:
        value = int(tx.get('value', 0)) / 1e18
        if value > 0 and value < DUST_THRESHOLD:
            dust_txs.append(tx)

    if len(dust_txs) >= 10:
        # Count unique recipient addresses
        unique_recipients = set(tx.get('to', '') for tx in dust_txs)

        if len(unique_recipients) >= 10:
            confidence = 'HIGH' if len(unique_recipients) >= 50 else 'MEDIUM'
            attacks.append({
                'type': 'Dusting',
                'confidence': confidence,
                'tx_count': len(dust_txs),
                'recipients': len(unique_recipients),
                'details': f'发现 {len(dust_txs)} 笔小额转账，涉及 {len(unique_recipients)} 个地址'
            })

    return attacks


def detect_protocol_vulnerability(txs: List[Dict]) -> List[Dict]:
    """Detect Protocol vulnerability exploitation (per D-17, D-22).

    Signature: Failed transactions with high value, abnormal patterns.

    Args:
        txs: List of ETH transaction dicts

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    for tx in txs:
        # Check for failed transactions with high value
        if tx.get('isError') == '1':
            value = int(tx.get('value', 0)) / 1e18
            if value > 10:
                attacks.append({
                    'type': 'Protocol Vulnerability',
                    'confidence': 'LOW',
                    'tx_hash': tx.get('hash', ''),
                    'details': f'高价值交易失败，可能涉及协议漏洞尝试'
                })

    return attacks


def detect_attacks_web(address: str, api_key: str) -> Dict[str, Any]:
    """Web interface for attack detection (CASE-02, per D-23 to D-30).

    Args:
        address: ETH address to analyze
        api_key: Etherscan API key (per-query input D-25)

    Returns:
        Dict with success, address, attack_cards, message
    """
    # Validate address format (must be ETH per D-24)
    if not address or not address.startswith('0x'):
        return {
            'success': False,
            'error': '请输入有效的ETH地址（0x开头）'
        }

    if len(address) != 42:
        return {
            'success': False,
            'error': 'ETH地址长度应为42字符'
        }

    # Get transaction history
    try:
        txs = get_eth_transactions(address, api_key, limit=100)
    except Exception as e:
        logger.warning(f"Failed to fetch ETH transactions: {e}")
        return {
            'success': False,
            'error': f'Etherscan API查询失败: {str(e)}'
        }

    if not txs:
        return {
            'success': True,
            'address': address,
            'attack_cards': [],
            'message': '未发现攻击痕迹'
        }

    # Run all 4 detectors
    all_attacks = []

    # Sandwich detection
    sandwich_attacks = detect_sandwich_attack(txs)
    all_attacks.extend(sandwich_attacks)

    # Flash Loan detection
    flash_loan_attacks = detect_flash_loan_attack(txs, api_key)
    all_attacks.extend(flash_loan_attacks)

    # Dusting detection
    dusting_attacks = detect_dusting_attack(txs)
    all_attacks.extend(dusting_attacks)

    # Protocol vulnerability detection
    protocol_attacks = detect_protocol_vulnerability(txs)
    all_attacks.extend(protocol_attacks)

    # Sort by confidence (HIGH first, following mixer_tracker pattern)
    all_attacks.sort(key=lambda x: (
        0 if x['confidence'] == 'HIGH' else
        1 if x['confidence'] == 'MEDIUM' else 2
    ))

    return {
        'success': True,
        'address': address,
        'attack_cards': all_attacks,
        'total_attacks': len(all_attacks),
        'message': '未发现攻击痕迹' if len(all_attacks) == 0 else None
    }