"""TRON address behavior analysis - 4 pattern analysis for criminal investigation"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict

# Import from core modules
from modules.core.api_client import get_trc20_transfers
from modules.core.formatter import format_timestamp, format_amount


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


def analyze_first_funding_source(address: str, transfers: List[Dict]) -> Dict[str, Any]:
    """Find first address that sent funds to this address.

    Args:
        address: TRON wallet address being analyzed
        transfers: List of TRC20 transfer records from Tronscan API

    Returns:
        dict with keys:
            - funder_address: str (first sender address)
            - first_transfer_time: int (timestamp in ms)
            - first_transfer_time_str: str (formatted datetime)
            - first_amount: str (formatted USDT amount)
            - first_amount_raw: float (raw USDT amount)
            - funder_tx_count: int (how many other transfers from this funder)
            - status: str ('无转入记录' if no incoming transfers)
    """
    if not transfers:
        return {'status': '无交易记录'}

    # Sort transfers by timestamp ascending (oldest first)
    sorted_transfers = sorted(
        transfers,
        key=lambda x: x.get('block_timestamp', 0) or 0
    )

    # Find first incoming transfer
    first_incoming = None
    for transfer in sorted_transfers:
        to_addr = transfer.get('to_address', '')
        if to_addr == address:
            first_incoming = transfer
            break

    if not first_incoming:
        return {'status': '无转入记录'}

    funder_address = first_incoming.get('from_address', '')
    first_timestamp = first_incoming.get('block_timestamp', 0)
    first_amount_raw = float(first_incoming.get('quant', 0)) / 1e6

    # Count how many other transfers from this funder
    funder_tx_count = sum(
        1 for t in transfers
        if t.get('from_address', '') == funder_address
    )

    return {
        'funder_address': funder_address,
        'first_transfer_time': first_timestamp,
        'first_transfer_time_str': format_timestamp(first_timestamp),
        'first_amount': format_amount(first_incoming.get('quant', 0)),
        'first_amount_raw': first_amount_raw,
        'funder_tx_count': funder_tx_count
    }


def analyze_transfer_patterns(address: str, transfers: List[Dict]) -> Dict[str, Any]:
    """Calculate in/out ratio and transfer frequency.

    Args:
        address: TRON wallet address being analyzed
        transfers: List of TRC20 transfer records from Tronscan API

    Returns:
        dict with keys:
            - total_in: str (formatted incoming USDT)
            - total_in_raw: float (raw incoming USDT)
            - total_out: str (formatted outgoing USDT)
            - total_out_raw: float (raw outgoing USDT)
            - in_out_ratio: float (total_in / total_out, 0 if no outgoing)
            - avg_transfer_interval_hours: float (average hours between transfers)
            - transfer_count_in: int (number of incoming transfers)
            - transfer_count_out: int (number of outgoing transfers)
            - status: str ('无交易记录' if no transfers)
    """
    if not transfers:
        return {'status': '无交易记录'}

    total_in_raw = 0.0
    total_out_raw = 0.0
    transfer_count_in = 0
    transfer_count_out = 0
    timestamps = []

    for transfer in transfers:
        from_addr = transfer.get('from_address', '')
        to_addr = transfer.get('to_address', '')
        amount_raw = float(transfer.get('quant', 0)) / 1e6
        timestamp = transfer.get('block_timestamp', 0)

        if timestamp:
            timestamps.append(timestamp)

        if to_addr == address:
            # Incoming transfer
            total_in_raw += amount_raw
            transfer_count_in += 1
        elif from_addr == address:
            # Outgoing transfer
            total_out_raw += amount_raw
            transfer_count_out += 1

    # Calculate in/out ratio (handle division by zero)
    if total_out_raw > 0:
        in_out_ratio = total_in_raw / total_out_raw
    else:
        in_out_ratio = 0.0 if total_in_raw == 0 else float('inf')

    # Calculate average transfer interval
    avg_interval_hours = 0.0
    if len(timestamps) >= 2:
        sorted_timestamps = sorted(timestamps)
        total_diff = 0
        for i in range(1, len(sorted_timestamps)):
            diff = sorted_timestamps[i] - sorted_timestamps[i-1]
            total_diff += diff
        avg_interval_hours = (total_diff / (len(timestamps) - 1)) / (1000 * 3600)

    return {
        'total_in': f"{total_in_raw:.2f}",
        'total_in_raw': total_in_raw,
        'total_out': f"{total_out_raw:.2f}",
        'total_out_raw': total_out_raw,
        'in_out_ratio': round(in_out_ratio, 2) if in_out_ratio != float('inf') else '无穷大',
        'avg_transfer_interval_hours': round(avg_interval_hours, 2),
        'transfer_count_in': transfer_count_in,
        'transfer_count_out': transfer_count_out
    }


def analyze_address_relationships(address: str, transfers: List[Dict]) -> Dict[str, Any]:
    """Identify frequently interacting addresses.

    Args:
        address: TRON wallet address being analyzed
        transfers: List of TRC20 transfer records from Tronscan API

    Returns:
        dict with keys:
            - top_counterparties: list of {address, interaction_count, total_amount}
            - unique_addresses_interacted: int (total unique addresses)
            - status: str ('无交易记录' if no transfers)
    """
    if not transfers:
        return {'status': '无交易记录'}

    # Count interactions per counterparty
    counterparties = defaultdict(lambda: {'count': 0, 'total_in': 0.0, 'total_out': 0.0})

    for transfer in transfers:
        from_addr = transfer.get('from_address', '')
        to_addr = transfer.get('to_address', '')
        amount_raw = float(transfer.get('quant', 0)) / 1e6

        if from_addr == address:
            # Outgoing to to_addr
            counterparties[to_addr]['count'] += 1
            counterparties[to_addr]['total_out'] += amount_raw
        elif to_addr == address:
            # Incoming from from_addr
            counterparties[from_addr]['count'] += 1
            counterparties[from_addr]['total_in'] += amount_raw

    # Calculate total amount for each counterparty and sort
    counterparty_list = []
    for addr, data in counterparties.items():
        counterparty_list.append({
            'address': addr,
            'interaction_count': data['count'],
            'total_amount': round(data['total_in'] + data['total_out'], 2),
            'total_in': round(data['total_in'], 2),
            'total_out': round(data['total_out'], 2)
        })

    # Sort by interaction count descending, take top 5
    counterparty_list.sort(key=lambda x: x['interaction_count'], reverse=True)
    top_counterparties = counterparty_list[:5]

    # Format addresses for display
    for cp in top_counterparties:
        if len(cp['address']) > 20:
            cp['address_short'] = f"{cp['address'][:8]}...{cp['address'][-4:]}"
        else:
            cp['address_short'] = cp['address']

    return {
        'top_counterparties': top_counterparties,
        'unique_addresses_interacted': len(counterparties)
    }


def analyze_activity_timeline(address: str, transfers: List[Dict]) -> Dict[str, Any]:
    """Build activity timeline with first/last activity and peak period.

    Args:
        address: TRON wallet address being analyzed
        transfers: List of TRC20 transfer records from Tronscan API

    Returns:
        dict with keys:
            - first_activity: int (timestamp in ms)
            - first_activity_str: str (formatted datetime)
            - last_activity: int (timestamp in ms)
            - last_activity_str: str (formatted datetime)
            - active_days: int (days between first and last activity)
            - peak_activity_period: dict {start, end, count, period_str}
            - total_transfers: int
            - status: str ('无交易记录' if no transfers)
    """
    if not transfers:
        return {'status': '无活动记录'}

    # Extract valid timestamps
    timestamps = []
    for transfer in transfers:
        ts = transfer.get('block_timestamp', 0)
        if ts and ts > 0:
            timestamps.append(ts)

    if not timestamps:
        return {'status': '无活动记录'}

    first_activity = min(timestamps)
    last_activity = max(timestamps)

    # Calculate active days
    time_diff_ms = last_activity - first_activity
    active_days = max(1, int(time_diff_ms / (1000 * 3600 * 24)) + 1)

    # Find peak activity period (7-day sliding window)
    if len(timestamps) == 1:
        peak_period = {
            'start': first_activity,
            'end': first_activity,
            'count': 1,
            'period_str': format_timestamp(first_activity).split()[0]
        }
    else:
        # Sort timestamps and find 7-day window with most activity
        sorted_timestamps = sorted(timestamps)
        window_ms = 7 * 24 * 3600 * 1000  # 7 days in milliseconds
        max_count = 0
        peak_start = sorted_timestamps[0]

        for i, start_ts in enumerate(sorted_timestamps):
            end_ts = start_ts + window_ms
            count = sum(1 for ts in sorted_timestamps if start_ts <= ts <= end_ts)
            if count > max_count:
                max_count = count
                peak_start = start_ts

        peak_end = peak_start + window_ms
        peak_period = {
            'start': peak_start,
            'end': peak_end,
            'count': max_count,
            'period_str': f"{format_timestamp(peak_start).split()[0]} 至 {format_timestamp(peak_end).split()[0]}"
        }

    return {
        'first_activity': first_activity,
        'first_activity_str': format_timestamp(first_activity),
        'last_activity': last_activity,
        'last_activity_str': format_timestamp(last_activity),
        'active_days': active_days,
        'peak_activity_period': peak_period,
        'total_transfers': len(timestamps)
    }


def analyze_behavior_web(address: str) -> Dict[str, Any]:
    """Web-friendly wrapper for TRON behavior analysis.

    Performs 4 behavior pattern analysis:
    1. First funding source (who first funded this address)
    2. Transfer patterns (in/out ratio, frequency)
    3. Address relationships (frequent counterparties)
    4. Activity timeline (first/last activity, active days)

    Args:
        address: TRON wallet address

    Returns:
        dict with keys:
            - success: bool
            - address: str
            - behaviors: dict with 4 pattern results (funding_source, transfer_patterns, relationships, timeline)
            - error: str (if success=False)
    """
    if not is_valid_tron_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的TRON地址格式（应以T开头，34位字符）',
            'behaviors': None
        }

    # Get transfer history (100 transfers for better analysis)
    transfers = get_trc20_transfers(address, limit=100)

    if not transfers:
        return {
            'success': True,
            'address': address,
            'behaviors': {
                'funding_source': {'status': '无转入记录'},
                'transfer_patterns': {'status': '无交易记录'},
                'relationships': {'status': '无交易对象'},
                'timeline': {'status': '无活动记录'}
            }
        }

    # Analyze 4 patterns
    behaviors = {
        'funding_source': analyze_first_funding_source(address, transfers),
        'transfer_patterns': analyze_transfer_patterns(address, transfers),
        'relationships': analyze_address_relationships(address, transfers),
        'timeline': analyze_activity_timeline(address, transfers)
    }

    return {
        'success': True,
        'address': address,
        'behaviors': behaviors
    }