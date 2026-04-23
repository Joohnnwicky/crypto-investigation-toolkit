"""Tronscan API client for TRON blockchain queries"""

import requests
from typing import Optional, Dict, List

TRONSCAN_BASE = "https://apilist.tronscanapi.com/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
DEFAULT_TIMEOUT = 10

def get_account_info(address: str) -> Optional[Dict]:
    """Get TRON address basic info from Tronscan API.

    Args:
        address: TRON wallet address (starts with 'T', 34 chars)

    Returns:
        dict with keys: address, balance, usdt_balance, total_transaction_count,
                        create_time, token_transfers, raw_data
        None if request fails
    """
    url = f"{TRONSCAN_BASE}/accountv2"
    params = {"address": address}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            return None
        data = response.json()

        # Calculate USDT balance from trc20 tokens
        usdt_balance = 0.0
        trc20_tokens = data.get('trc20token_balances', [])
        for token in trc20_tokens:
            if token.get('tokenId') == USDT_CONTRACT:
                usdt_balance = int(token.get('balance', 0)) / 1e6
                break

        return {
            'address': address,
            'balance': data.get('balance', 0) / 1e6,
            'usdt_balance': usdt_balance,
            'total_transaction_count': data.get('total_transaction_count', 0),
            'create_time': data.get('create_time', 0),
            'token_transfers': trc20_tokens,
            'raw_data': data
        }
    except Exception:
        return None

def get_trc20_transfers(address: str, limit: int = 50) -> List[Dict]:
    """Get TRC20 token transfer history for an address.

    Args:
        address: TRON wallet address
        limit: Maximum number of transfers to fetch (default 50)

    Returns:
        list of transfer dicts with keys: block_timestamp, from_address,
                                          to_address, quant, tokenInfo
    """
    url = f"{TRONSCAN_BASE}/token_trc20/transfers"
    params = {
        "relatedAddress": address,
        "limit": limit,
        "sort": "-timestamp"
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get('token_transfers', [])
    except Exception:
        return []