"""Obfuscation attack detection module for ETH chain attack pattern analysis"""

import logging
from typing import Dict, List, Any

from modules.core.api_client import get_eth_transactions, get_erc20_transfers

logger = logging.getLogger(__name__)

# DEX Router addresses for Sandwich detection
DEX_ROUTERS = {
    'uniswap_v2': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
    'uniswap_v3': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
    'universal': '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD',
    'sushiswap': '0xd9e1cE17f2641f24AE83637ab58a1aFa2493E64',
}

# Dust threshold for Dusting detection (per D-21)
DUST_THRESHOLD = 0.001  # ETH


def detect_sandwich_attack(txs: List[Dict]) -> List[Dict]:
    """Detect possible sandwich participation (per D-14, D-20).

    A sandwich attack involves three transactions (frontrun, victim, backrun)
    across *different* addresses, which cannot be confirmed from a single
    address's history. We conservatively flag only when the analyzed
    address itself makes mixed-direction swaps (ETH-in and token-out) to
    the same DEX router within one block - a possible self-sandwich
    pattern that still needs manual confirmation.

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
            block_groups.setdefault(block, []).append(tx)

    dex_addresses_lower = [addr.lower() for addr in DEX_ROUTERS.values()]

    for block, block_txs in block_groups.items():
        dex_txs = [t for t in block_txs if t.get('to', '').lower() in dex_addresses_lower]

        if len(dex_txs) >= 2:
            has_eth_in = any(int(t.get('value', 0)) > 0 for t in dex_txs)
            has_token_swap = any(int(t.get('value', 0)) == 0 for t in dex_txs)

            # Mixed directions in one block to the same router
            if has_eth_in and has_token_swap:
                attacks.append({
                    'type': '疑似三明治参与(待复核)',
                    'confidence': 'LOW',
                    'block': block,
                    'tx_count': len(dex_txs),
                    'details': f'区块 {block} 内该地址对同一 DEX 路由有混合方向 Swap（ETH入+代币出）。单地址视角无法确认三明治，需结合受害地址与多地址关联复核。'
                })

    return attacks


def detect_flash_loan_attack(txs: List[Dict], api_key: str) -> List[Dict]:
    """Flag high-value transactions for manual flash-loan review.

    A flash loan is a borrow-repay within a single transaction and cannot
    be identified by ETH value alone (net ETH movement is often zero).
    The previous "value > 100 ETH => Flash Loan HIGH" was a false positive
    generator. We now only flag large-value txs for review, not as
    confirmed flash loans.

    Args:
        txs: List of ETH transaction dicts
        api_key: Etherscan API key (reserved; log analysis not implemented)

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    for tx in txs:
        value = int(tx.get('value', 0)) / 1e18

        # High value transactions (> 100 ETH) - review candidate only
        if value > 100:
            attacks.append({
                'type': '大额交易(待复核)',
                'confidence': 'LOW',
                'tx_hash': tx.get('hash', ''),
                'value': value,
                'details': f'交易金额 {value:.2f} ETH，金额较大。是否涉及闪贷需解析交易日志（借贷协议调用+同笔归还）确认，不可仅凭金额判定。'
            })

    return attacks


def detect_dusting_attack(txs: List[Dict]) -> List[Dict]:
    """Detect Dusting attack patterns (per D-16, D-21).

    Flags many outgoing ETH transfers with tiny amounts to many different
    addresses. Note: ERC20 token dusting is NOT visible here because
    Etherscan normal txs carry value=0 for token transfers.

    Args:
        txs: List of ETH transaction dicts

    Returns:
        List of attack dicts with type, confidence, details
    """
    attacks = []

    # Filter outgoing ETH transactions with tiny values
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
                'details': f'发现 {len(dust_txs)} 笔小额 ETH 转账，涉及 {len(unique_recipients)} 个地址。仅覆盖 ETH 转账，ERC20 代币粉尘未纳入。'
            })

    return attacks


def detect_protocol_vulnerability(txs: List[Dict]) -> List[Dict]:
    """Flag failed high-value transactions for review (per D-17, D-22).

    A failed high-value transaction may indicate a protocol exploit attempt,
    but failure alone is not confirmation. Flagged for manual review only.

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
                    'type': '失败交易(待复核)',
                    'confidence': 'LOW',
                    'tx_hash': tx.get('hash', ''),
                    'value': value,
                    'details': f'高价值交易失败（{value:.2f} ETH），可能涉及协议漏洞尝试，需结合交易日志与合约状态复核。'
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