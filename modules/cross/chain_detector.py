"""Chain type detection module for TRON/ETH/BTC addresses"""

import re
from typing import Dict


def detect_chain_type(address: str) -> str:
    """Detect blockchain type from address format.

    Args:
        address: Wallet address string

    Returns:
        Chain type string: 'tron', 'eth', 'btc', or 'unknown'
    """
    if not address:
        return 'unknown'

    # TRON: Starts with 'T', 34 chars total
    if re.match(r'^T[A-Za-z1-9]{33}$', address):
        return 'tron'

    # ETH: Starts with '0x', 40 hex chars
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return 'eth'

    # BTC patterns (from btc_analyzer.py identify_address_type)
    # P2PKH: Legacy address starting with 1
    if re.match(r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'

    # P2SH: Script hash address starting with 3
    if re.match(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'

    # P2WPKH: Native SegWit bc1q...
    if re.match(r'^bc1q[ac-hj-np-z02-9]{39,59}$', address.lower()):
        return 'btc'

    # P2TR: Taproot bc1p...
    if re.match(r'^bc1p[ac-hj-np-z02-9]{58}$', address.lower()):
        return 'btc'

    return 'unknown'


def validate_address_format(address: str) -> bool:
    """Validate if address matches any known format.

    Args:
        address: Wallet address string

    Returns:
        True if valid format, False otherwise
    """
    return detect_chain_type(address) != 'unknown'


def get_chain_requirements(chain: str) -> Dict:
    """Get API requirements for a chain type.

    Args:
        chain: Chain type string ('tron', 'eth', 'btc')

    Returns:
        Dict with requires_key, api_name, key_placeholder
    """
    if chain == 'tron':
        return {
            'requires_key': False,
            'api_name': 'Tronscan',
            'key_placeholder': ''
        }
    elif chain == 'eth':
        return {
            'requires_key': True,
            'api_name': 'Etherscan',
            'key_placeholder': '从 etherscan.io 获取免费API密钥'
        }
    elif chain == 'btc':
        return {
            'requires_key': False,
            'api_name': 'Blockstream',
            'key_placeholder': ''
        }
    else:
        return {
            'requires_key': False,
            'api_name': 'Unknown',
            'key_placeholder': ''
        }