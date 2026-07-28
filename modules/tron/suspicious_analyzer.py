"""TRON address suspicious feature analysis - adapted from CLI script"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import from core modules
from modules.core.api_client import get_account_info, get_trc20_transfers
from modules.core.formatter import format_days_since_creation

def is_valid_tron_address(address: str) -> bool:
    """Validate TRON address format.

    Args:
        address: Potential TRON address

    Returns:
        True if address matches TRON format (T prefix, 34 chars, Base58)
    """
    if not address:
        return False
    return bool(re.match(r'^T[A-Za-z1-9]{33}$', address))

def detect_suspicious_features(address_info: Optional[Dict], trc20_transfers: List[Dict]) -> Dict[str, Any]:
    """Identify suspicious features for fraud/money laundering detection.

    Adapted from lines 170-352 of 001-day1-TRON地址可疑特征分析工具.py

    Args:
        address_info: Address basic info from get_account_info
        trc20_transfers: TRC20 transfer history from get_trc20_transfers

    Returns:
        dict with keys:
            - red: list of high-risk alerts
            - yellow: list of medium-risk alerts
            - green: list of normal-range features
            - score: 0-100 risk score
    """
    alerts = {
        'red': [],
        'yellow': [],
        'green': [],
        'score': 0
    }

    if not address_info:
        alerts['red'].append({
            'feature': '查询失败',
            'detail': '无法获取地址信息，请检查地址是否正确',
            'meaning': '可能地址不存在或API暂时不可用'
        })
        return alerts

    usdt_balance = address_info.get('usdt_balance', 0)
    trx_balance = address_info.get('balance', 0)
    total_tx = address_info.get('total_transaction_count', 0)
    create_time = address_info.get('create_time', 0)

    # Whether this address ever received USDT (avoids false "余额清空" on
    # TRX-only wallets that never held USDT).
    ever_held_usdt = any(
        t.get('to_address', '') == address_info['address']
        for t in (trc20_transfers or [])
    )

    # RED ALERT: Balance emptied (previously held USDT, now zero)
    if usdt_balance == 0 and ever_held_usdt:
        alerts['red'].append({
            'feature': '余额清空',
            'detail': f'曾持有USDT，当前余额已清零: {usdt_balance:.2f} USDT',
            'meaning': '资金已被转移，需追踪流向（仅供参考，非司法证据）'
        })
        alerts['score'] += 20

    # YELLOW: coverage blind spot - only TRC20(USDT) is analyzed
    alerts['yellow'].append({
        'feature': '分析范围说明',
        'detail': '本工具仅分析 TRC20(USDT) 转账记录',
        'meaning': 'TRX/TRC10/内部合约交易未覆盖，存在盲区'
    })

    # RED ALERT: Recently created address with transactions
    days_since_create = format_days_since_creation(create_time)
    if days_since_create <= 7 and days_since_create > 0 and total_tx > 0:
        alerts['red'].append({
            'feature': '创建时间短',
            'detail': f'地址创建于 {days_since_create} 天前，已有 {total_tx} 笔交易',
            'meaning': '可能是专门用于诈骗的"一次性地址"'
        })
        alerts['score'] += 25

    # RED ALERT: Large transfer in + immediate transfer out (快进快出)
    # Sort ascending by timestamp so we can look FORWARD in time for the
    # outgoing leg. The previous implementation iterated API (descending)
    # order and computed time_diff backwards, so it never triggered.
    if trc20_transfers and len(trc20_transfers) >= 2:
        large_in_threshold = 1000  # USDT
        quick_transfer_hours = 24

        sorted_transfers = sorted(
            trc20_transfers,
            key=lambda x: x.get('block_timestamp', 0) or 0
        )

        found_fast_out = False
        for i, transfer in enumerate(sorted_transfers):
            try:
                amount = float(transfer.get('quant', 0)) / 1e6
                to_addr = transfer.get('to_address', '')
                in_timestamp = transfer.get('block_timestamp', 0)

                # Large incoming transfer to this address
                if to_addr == address_info['address'] and amount >= large_in_threshold:
                    # Look FORWARD for an outgoing transfer within the window
                    for j in range(i + 1, len(sorted_transfers)):
                        later = sorted_transfers[j]
                        if later.get('from_address', '') != address_info['address']:
                            continue
                        out_amount = float(later.get('quant', 0)) / 1e6
                        if out_amount <= 0:
                            continue
                        out_timestamp = later.get('block_timestamp', 0)
                        time_diff_hours = (out_timestamp - in_timestamp) / (1000 * 3600)

                        if 0 < time_diff_hours <= quick_transfer_hours:
                            alerts['red'].append({
                                'feature': '大额转入+立即转出',
                                'detail': f'转入 {amount:.2f} USDT 后 {time_diff_hours:.1f} 小时内转出 {out_amount:.2f} USDT',
                                'meaning': '典型洗钱模式（快进快出），仅供参考，非司法证据'
                            })
                            alerts['score'] += 35
                            found_fast_out = True
                            break
                    if found_fast_out:
                        break
            except (ValueError, TypeError):
                continue

    # YELLOW ALERT: Multiple small incoming transfers from different addresses
    if trc20_transfers:
        small_in_count = 0
        in_addresses = set()

        for transfer in trc20_transfers:
            try:
                amount = float(transfer.get('quant', 0)) / 1e6
                to_addr = transfer.get('to_address', '')

                if to_addr == address_info['address'] and amount < 100:
                    small_in_count += 1
                    in_addresses.add(transfer.get('from_address', ''))
            except (ValueError, TypeError):
                continue

        if small_in_count >= 3 and len(in_addresses) >= 2:
            alerts['yellow'].append({
                'feature': '多笔小额转入',
                'detail': f'收到 {small_in_count} 笔小额转账，来自 {len(in_addresses)} 个不同地址',
                'meaning': '典型的"归集"行为，可能来自多个受害者'
            })
            alerts['score'] += 15

    # YELLOW ALERT: Dispersed transfers out
    if trc20_transfers:
        out_addresses = set()
        for transfer in trc20_transfers:
            try:
                from_addr = transfer.get('from_address', '')
                if from_addr == address_info['address']:
                    out_addresses.add(transfer.get('to_address', ''))
            except (ValueError, TypeError):
                continue

        if len(out_addresses) >= 3:
            alerts['yellow'].append({
                'feature': '分散转出',
                'detail': f'资金被转出到 {len(out_addresses)} 个不同地址',
                'meaning': '洗钱操作，资金已分散'
            })
            alerts['score'] += 20

    # GREEN ALERTS: Normal features
    if usdt_balance > 0:
        alerts['green'].append({
            'feature': '余额稳定',
            'detail': f'USDT余额: {usdt_balance:.2f} USDT',
            'meaning': '资金仍在地址中，可联系交易所冻结'
        })

    if trx_balance > 10:
        alerts['green'].append({
            'feature': '少量TRX',
            'detail': f'TRX余额: {trx_balance:.2f} TRX',
            'meaning': '地址仍在使用中'
        })

    if 5 <= total_tx <= 100:
        alerts['green'].append({
            'feature': '交易数适中',
            'detail': f'总交易数: {total_tx}',
            'meaning': '符合正常使用模式'
        })

    # Cap score at 100
    alerts['score'] = min(alerts['score'], 100)

    # Map raw additive score to a coarse risk level. The score is an
    # uncalibrated heuristic sum; expose it only as low/mid/high, not as a
    # precise figure, to avoid false precision in a forensic context.
    score = alerts['score']
    if score >= 61:
        alerts['risk_level'] = '高'
    elif score >= 31:
        alerts['risk_level'] = '中'
    else:
        alerts['risk_level'] = '低'

    return alerts

def analyze_address_web(address: str) -> Dict[str, Any]:
    """Web-friendly wrapper for full address analysis.

    Args:
        address: TRON wallet address

    Returns:
        dict with keys:
            - success: bool
            - address: str
            - basic_info: dict (balance, usdt_balance, total_transaction_count, create_time)
            - alerts: dict (red, yellow, green, score)
            - error: str (if success=False)
    """
    if not is_valid_tron_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的TRON地址格式（应以T开头，34位字符）',
            'basic_info': None,
            'alerts': None
        }

    basic_info = get_account_info(address)
    if not basic_info:
        return {
            'success': False,
            'address': address,
            'error': '无法获取地址信息，请稍后重试',
            'basic_info': None,
            'alerts': None
        }

    trc20_transfers = get_trc20_transfers(address, limit=50)
    alerts = detect_suspicious_features(basic_info, trc20_transfers)

    return {
        'success': True,
        'address': address,
        'basic_info': {
            'balance': basic_info.get('balance', 0),
            'usdt_balance': basic_info.get('usdt_balance', 0),
            'total_transaction_count': basic_info.get('total_transaction_count', 0),
            'create_time': basic_info.get('create_time', 0)
        },
        'alerts': alerts
    }