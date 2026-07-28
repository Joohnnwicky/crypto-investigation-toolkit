"""Tronscan and Etherscan API clients for blockchain queries"""

import logging
import requests
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# Tronscan API configuration
TRONSCAN_BASE = "https://api.tronscan.org/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
DEFAULT_TIMEOUT = 10

# Etherscan API V2 configuration (V1 deprecated)
ETHERSCAN_BASE = "https://api.etherscan.io/v2/api"
ETH_CHAIN_ID = "1"  # Ethereum mainnet

def get_account_info(address: str) -> Optional[Dict]:
    """Get TRON address basic info from Tronscan API.

    Args:
        address: TRON wallet address (starts with 'T', 34 chars)

    Returns:
        dict with keys: address, balance, usdt_balance, total_transaction_count,
                        create_time, token_transfers, raw_data
        None if request fails
    """
    url = f"{TRONSCAN_BASE}/account"
    params = {"address": address}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"Tronscan account API returned {response.status_code} for {address}")
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
    except Exception as e:
        logger.warning(f"get_account_info failed for {address}: {e}")
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
            logger.warning(f"Tronscan trc20 API returned {response.status_code} for {address}")
            return []
        data = response.json()
        return data.get('token_transfers', [])
    except Exception as e:
        logger.warning(f"get_trc20_transfers failed for {address}: {e}")
        return []

def get_eth_transactions(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """Get normal ETH transactions for an address from Etherscan API.

    Args:
        address: ETH wallet address (0x prefix, 40 hex chars)
        api_key: User-provided Etherscan API key (per-query input, never stored)
        limit: Maximum number of transactions to fetch (default 100)

    Returns:
        list of transaction dicts with keys: blockNumber, timeStamp, hash,
                                            from, to, value, gas, gasUsed, isError
        Empty list if request fails or no transactions
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "account",
        "action": "txlist",
        "address": address,
        "apikey": api_key,
        "page": 1,
        "offset": limit,
        "sort": "desc"
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"Etherscan txlist API returned {response.status_code} for {address}")
            return []
        data = response.json()

        # Etherscan returns status='1' for success, '0' for error/no results
        if data.get('status') != '1':
            logger.info(f"Etherscan txlist returned no results for {address}: {data.get('message', '')}")
            return []

        return data.get('result', [])
    except Exception as e:
        logger.warning(f"get_eth_transactions failed for {address}: {e}")
        return []

def get_eth_balance(address: str, api_key: str) -> Optional[float]:
    """Get current ETH balance (in ether) for an address from Etherscan API.

    Uses the lightweight balance endpoint (single call, free-tier friendly)
    instead of estimating from transaction history, which is unreliable
    (no internal txs, no gas subtraction, limited window).

    Args:
        address: ETH wallet address (0x prefix, 40 hex chars)
        api_key: User-provided Etherscan API key (per-query input, never stored)

    Returns:
        Balance in ETH, or None if the request fails.
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_key,
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"Etherscan balance API returned {response.status_code} for {address}")
            return None
        data = response.json()
        if data.get('status') != '1':
            logger.info(f"Etherscan balance returned non-success for {address}: {data.get('message', '')}")
            return None
        return int(data.get('result', 0)) / 1e18
    except Exception as e:
        logger.warning(f"get_eth_balance failed for {address}: {e}")
        return None


def get_erc20_transfers(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """Get ERC20 token transfers for an address from Etherscan API.

    Args:
        address: ETH wallet address (0x prefix, 40 hex chars)
        api_key: User-provided Etherscan API key (per-query input, never stored)
        limit: Maximum number of transfers to fetch (default 100)

    Returns:
        list of transfer dicts with keys: blockNumber, timeStamp, hash,
                                          from, to, value, tokenSymbol,
                                          tokenName, tokenDecimal
        Empty list if request fails or no transfers
    """
    params = {
        "chainid": ETH_CHAIN_ID,
        "module": "account",
        "action": "tokentx",
        "address": address,
        "apikey": api_key,
        "page": 1,
        "offset": limit,
        "sort": "desc"
    }

    try:
        response = requests.get(ETHERSCAN_BASE, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"Etherscan tokentx API returned {response.status_code} for {address}")
            return []
        data = response.json()

        # Etherscan returns status='1' for success, '0' for error/no results
        if data.get('status') != '1':
            logger.info(f"Etherscan tokentx returned no results for {address}: {data.get('message', '')}")
            return []

        return data.get('result', [])
    except Exception as e:
        logger.warning(f"get_erc20_transfers failed for {address}: {e}")
        return []
