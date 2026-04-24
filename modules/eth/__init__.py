"""ETH module initialization"""

from .eth_analyzer import query_eth_transactions_web, is_valid_eth_address
from .stargate_detector import detect_stargate_bridge, STARGATE_CONTRACTS

__all__ = [
    'query_eth_transactions_web',
    'is_valid_eth_address',
    'detect_stargate_bridge',
    'STARGATE_CONTRACTS'
]