"""Multi-chain address monitoring module for TRON/ETH/BTC status tracking"""

import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

from modules.cross.chain_detector import detect_chain_type, get_chain_requirements
from modules.core.api_client import get_account_info, get_trc20_transfers, get_eth_transactions

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10


def get_btc_address_stats(address: str) -> Optional[Dict]:
    """Get BTC address stats from Blockstream API.

    Args:
        address: BTC wallet address (1..., 3..., or bc1... format)

    Returns:
        Dict with address, balance, tx_count, total_received
        None if request fails
    """
    url = f"https://blockstream.info/api/address/{address}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"Blockstream API error for {address}: {response.status_code}")
            return None

        data = response.json()

        # Extract chain_stats
        chain_stats = data.get('chain_stats', {})
        funded_txo_sum = chain_stats.get('funded_txo_sum', 0)
        spent_txo_sum = chain_stats.get('spent_txo_sum', 0)

        # Calculate balance in BTC (satoshis to BTC)
        balance = (funded_txo_sum - spent_txo_sum) / 1e8
        tx_count = chain_stats.get('tx_count', 0)

        return {
            'address': address,
            'balance': balance,
            'tx_count': tx_count,
            'total_received': funded_txo_sum / 1e8
        }
    except Exception as e:
        logger.warning(f"Failed to fetch BTC stats for {address}: {e}")
        return None


def monitor_addresses_web(addresses: List[str], eth_key: str = '') -> Dict[str, Any]:
    """Web interface for multi-chain address monitoring.

    Args:
        addresses: List of wallet addresses (max 10 per D-04)
        eth_key: Etherscan API key (required for ETH addresses, per-query input D-06)

    Returns:
        Dict with success, addresses, status_cards, total_count, error
    """
    # Validate addresses (D-04: max 10)
    if not addresses:
        return {'success': False, 'error': '请输入至少一个地址'}

    # Clean addresses: strip whitespace, filter empty
    addresses = [addr.strip() for addr in addresses if addr.strip()]

    if len(addresses) > 10:
        return {'success': False, 'error': '地址数量超过10个限制'}

    # Detect chain types and validate (D-05)
    address_chain_map = {}
    needs_eth_key = False

    for addr in addresses:
        chain = detect_chain_type(addr)
        if chain == 'unknown':
            return {'success': False, 'error': f'无法识别地址链类型: {addr}'}
        address_chain_map[addr] = chain
        if chain == 'eth':
            needs_eth_key = True

    # Validate API keys (D-06)
    eth_key = eth_key.strip()
    if needs_eth_key and not eth_key:
        return {'success': False, 'error': 'ETH地址需要Etherscan API密钥'}

    # Fetch status for each address
    status_cards = []

    for addr in addresses:
        chain = address_chain_map[addr]
        card = {
            'address': addr,
            'chain': chain,
            'balance': 0,
            'tx_count': 0,
            'last_active': '未知',
            'error': None
        }

        try:
            if chain == 'tron':
                # TRON: Use Tronscan API
                account_info = get_account_info(addr)
                if account_info:
                    # Get TRX balance
                    card['balance'] = account_info.get('balance', 0)
                    card['tx_count'] = account_info.get('total_transaction_count', 0)

                    # Get last active time from recent transfers
                    transfers = get_trc20_transfers(addr, limit=1)
                    if transfers:
                        ts = transfers[0].get('block_timestamp', 0)
                        if ts > 0:
                            card['last_active'] = datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M')
                    elif account_info.get('create_time', 0) > 0:
                        # Use create_time as fallback
                        card['last_active'] = datetime.fromtimestamp(account_info['create_time'] / 1000).strftime('%Y-%m-%d')

            elif chain == 'eth':
                # ETH: Use Etherscan API
                eth_txs = get_eth_transactions(addr, eth_key, limit=100)
                if eth_txs:
                    # Calculate balance from transaction values
                    balance = 0.0
                    for tx in eth_txs:
                        value = int(tx.get('value', 0)) / 1e18
                        if tx.get('to', '').lower() == addr.lower():
                            balance += value
                        elif tx.get('from', '').lower() == addr.lower():
                            balance -= value

                    card['balance'] = balance
                    card['tx_count'] = len(eth_txs)

                    # Last active from most recent transaction
                    first_tx = eth_txs[0]
                    ts = int(first_tx.get('timeStamp', 0))
                    if ts > 0:
                        card['last_active'] = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                else:
                    # No transactions found
                    card['last_active'] = '无交易记录'

            elif chain == 'btc':
                # BTC: Use Blockstream API
                btc_stats = get_btc_address_stats(addr)
                if btc_stats:
                    card['balance'] = btc_stats.get('balance', 0)
                    card['tx_count'] = btc_stats.get('tx_count', 0)
                    # Blockstream doesn't provide timestamps directly
                    card['last_active'] = '需单独查询'
                else:
                    card['error'] = 'Blockstream API查询失败'

        except Exception as e:
            logger.warning(f"Failed to fetch status for {addr}: {e}")
            card['error'] = str(e)

        status_cards.append(card)

    return {
        'success': True,
        'addresses': addresses,
        'status_cards': status_cards,
        'total_count': len(status_cards)
    }