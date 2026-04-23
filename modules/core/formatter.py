"""Data formatting utilities for blockchain analysis results"""

from datetime import datetime
from typing import Optional, Union

def format_timestamp(timestamp_ms: Union[int, float, None]) -> str:
    """Convert millisecond timestamp to human-readable datetime string.

    Args:
        timestamp_ms: Timestamp in milliseconds (from Tronscan API)

    Returns:
        Formatted string like "2024-01-15 14:30:00"
        "未知" if timestamp is None or invalid
    """
    if timestamp_ms is None or timestamp_ms == 0:
        return "未知"

    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "未知"

def format_amount(amount_raw: Union[int, float, None], decimals: int = 6) -> str:
    """Convert raw token amount to human-readable string.

    Args:
        amount_raw: Raw amount (needs division by 10^decimals)
        decimals: Token decimals (default 6 for USDT TRC20)

    Returns:
        Formatted string like "1234.56 USDT"
        "0" if amount is None or 0
    """
    if amount_raw is None:
        return "0"

    try:
        actual_amount = float(amount_raw) / (10 ** decimals)
        return f"{actual_amount:.2f}"
    except (ValueError, TypeError):
        return "0"

def format_days_since_creation(create_time_ms: Union[int, float, None]) -> int:
    """Calculate days since address creation.

    Args:
        create_time_ms: Creation timestamp in milliseconds

    Returns:
        Number of days since creation (0 if invalid)
    """
    if create_time_ms is None or create_time_ms == 0:
        return 0

    try:
        create_dt = datetime.fromtimestamp(create_time_ms / 1000)
        days = (datetime.now() - create_dt).days
        return max(0, days)
    except (ValueError, TypeError):
        return 0

def format_tron_address(address: str) -> str:
    """Format TRON address for display (truncate middle if too long).

    Args:
        address: Full TRON address

    Returns:
        Truncated like "TUtPdo...NNw" if > 20 chars
        Original if shorter
    """
    if not address or len(address) <= 20:
        return address or ""
    return f"{address[:8]}...{address[-4:]}"