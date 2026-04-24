"""Uniswap V2 DEX tracing module for Swap transaction analysis"""

import logging
import re
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    Web3 = None

from modules.core.eth_rpc_client import EthRpcClient

# Configure logging
logger = logging.getLogger(__name__)

# Etherscan API configuration (V2 API with chainid)
ETHERSCAN_API_URL = "https://api.etherscan.io/v2/api"
ETH_CHAIN_ID = "1"

# Major token addresses (from canonical script)
TOKENS = {
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI": "0x6B175474E89094C44Da98b954EeadeCB5BE3830"
}

# ERC-20 Transfer event signature (from canonical script line 30)
TRANSFER_EVENT_SIG = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df35bcf8"

# Uniswap V2 Router address (from canonical script line 39)
ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

# Request timeout
DEFAULT_TIMEOUT = 10


def validate_eth_address(address: str) -> bool:
    """Validate ETH address format.

    Args:
        address: ETH address string

    Returns:
        True if valid (0x + 40 hex chars), False otherwise
    """
    if not address:
        return False
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))


class UniswapTracker:
    """Uniswap V2 Swap transaction tracker.

    Parses Swap transactions to identify token pairs and amounts.
    """

    def __init__(self):
        """Initialize tracker with EthRpcClient."""
        self.rpc_client = EthRpcClient()
        self.w3: Optional[Web3] = None

    def _get_w3(self) -> Web3:
        """Get Web3 instance."""
        if self.w3 is None:
            self.w3 = self.rpc_client.get_web3()
        return self.w3

    def get_token_decimals(self, token_address: str) -> int:
        """Get token decimals from contract.

        Args:
            token_address: Token contract address

        Returns:
            Decimals (e.g., USDT=6, ETH=18)
        """
        # Known tokens have fixed decimals
        for name, addr in TOKENS.items():
            if addr.lower() == token_address.lower():
                if name in ["USDT", "USDC"]:
                    return 6
                return 18

        # Query contract for unknown tokens
        try:
            w3 = self._get_w3()
            contract = w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=[{
                    "inputs": [],
                    "name": "decimals",
                    "outputs": [{"name": "", "type": "uint8"}],
                    "stateMutability": "view",
                    "type": "function"
                }]
            )
            return contract.functions.decimals().call()
        except Exception as e:
            logger.warning(f"Failed to get decimals for {token_address}: {e}")
            return 18  # Default to 18

    def format_token_amount(self, amount: int, decimals: int) -> str:
        """Format token amount for display.

        Args:
            amount: Raw token amount (wei/smallest unit)
            decimals: Token decimals

        Returns:
            Human-readable amount string
        """
        value = amount / (10 ** decimals)
        if decimals <= 6:
            return f"{value:,.{decimals}f}"
        return f"{value:,.4f}"

    def _get_token_name(self, token_address: str) -> str:
        """Get token name from address.

        Args:
            token_address: Token contract address

        Returns:
            Token name (e.g., "USDT") or abbreviated address
        """
        for name, addr in TOKENS.items():
            if addr.lower() == token_address.lower():
                return name
        return f"Token({token_address[:10]}...)"

    def parse_swap_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Parse single Swap transaction.

        Args:
            tx_hash: Transaction hash (66 hex chars with 0x prefix)

        Returns:
            Dict with hash, from, to, value, logs, swap_type
        """
        try:
            w3 = self._get_w3()
            tx = w3.eth.get_transaction(tx_hash)
            receipt = w3.eth.get_transaction_receipt(tx_hash)

            result = {
                "hash": tx_hash,
                "from": tx['from'],
                "to": tx['to'],
                "value": float(w3.from_wei(tx['value'], 'ether')),
                "block_number": receipt['blockNumber'],
                "status": "success" if receipt['status'] == 1 else "failed",
                "logs": []
            }

            # Parse Transfer events from receipt logs
            for log in receipt['logs']:
                if len(log['topics']) < 3:
                    continue

                topic0 = log['topics'][0].hex()

                if topic0 == TRANSFER_EVENT_SIG:
                    from_addr = "0x" + log['topics'][1].hex()[26:]
                    to_addr = "0x" + log['topics'][2].hex()[26:]
                    value = int(log['data'], 16) if log['data'] else 0

                    result['logs'].append({
                        "event": "Transfer",
                        "from": Web3.to_checksum_address(from_addr),
                        "to": Web3.to_checksum_address(to_addr),
                        "value": value,
                        "token_address": log['address']
                    })

            # Identify swap type
            result['swap_type'] = self.identify_swap_type(result)
            return result

        except Exception as e:
            logger.error(f"Failed to parse transaction {tx_hash}: {e}")
            return {"hash": tx_hash, "error": str(e), "status": "failed"}

    def identify_swap_type(self, tx_info: Dict[str, Any]) -> str:
        """Identify Swap type from transaction logs.

        Args:
            tx_info: Parsed transaction info

        Returns:
            Swap type description (e.g., "ETH -> USDT")
        """
        logs = tx_info.get('logs', [])
        if not logs:
            return "未知"

        # Check if transaction is to Uniswap Router
        if tx_info.get('to') and tx_info['to'].lower() == ROUTER_ADDRESS.lower():
            # Analyze token flow
            tokens_in = []
            tokens_out = []

            for log in logs:
                token_addr = log['token_address']
                token_name = self._get_token_name(token_addr)
                decimals = self.get_token_decimals(token_addr)
                amount = self.format_token_amount(log['value'], decimals)

                # Token sent to router = token sold
                if log['to'].lower() == ROUTER_ADDRESS.lower():
                    tokens_out.append(f"{amount} {token_name}")
                # Token from router = token received
                elif log['from'].lower() == ROUTER_ADDRESS.lower():
                    tokens_in.append(f"{amount} {token_name}")

            # ETH swap (value > 0)
            if tx_info.get('value', 0) > 0:
                tokens_out.append(f"{tx_info['value']} ETH")

            if tokens_in and tokens_out:
                return f"{' + '.join(tokens_out)} -> {' + '.join(tokens_in)}"
            elif tokens_in:
                return f"ETH -> {' + '.join(tokens_in)}"
            elif tokens_out:
                return f"{' + '.join(tokens_out)} -> ETH"

        return "普通转账"

    def generate_flow_diagram(self, swaps: List[Dict[str, Any]]) -> str:
        """Generate ASCII flow diagram for swaps.

        Args:
            swaps: List of swap transactions

        Returns:
            ASCII diagram string
        """
        if not swaps:
            return "无Swap交易记录"

        diagram = """
┌─────────────────────────────────────────────────────────────┐
│  Uniswap Swap 追踪结果                                        │
├─────────────────────────────────────────────────────────────┤"""

        for i, swap in enumerate(swaps[:10]):  # Limit to 10 for readability
            diagram += f"""
│  [{i+1}] {swap.get('type', 'Swap')}                             │
│      时间: {swap.get('time', '未知')}                           │
│      输入: {swap.get('amount_in', '未知')}                      │
│      输出: {swap.get('amount_out', '未知')}                     │"""

        diagram += """
└─────────────────────────────────────────────────────────────┘
"""
        return diagram

    def get_address_transactions(self, address: str, api_key: str, limit: int = 50) -> List[Dict]:
        """Get transactions for address and identify Swap transactions.

        Args:
            address: ETH address to query
            api_key: Etherscan API key
            limit: Max transactions to analyze

        Returns:
            List of identified Swap transactions
        """
        swaps = []
        txs = get_eth_transactions(address, api_key, limit)

        for tx in txs:
            # Check if transaction is to Uniswap Router
            to_addr = tx.get('to', '')
            if to_addr and to_addr.lower() == ROUTER_ADDRESS.lower():
                # Parse timestamp
                ts = tx.get('timeStamp', '')
                if ts:
                    try:
                        time_str = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = "未知"
                else:
                    time_str = "未知"

                # Determine swap type based on value
                value_eth = float(tx.get('value', 0)) / 1e18 if tx.get('value') else 0

                if value_eth > 0:
                    swap_type = f"ETH -> Token"
                    amount_in = f"{value_eth:.4f} ETH"
                else:
                    swap_type = "Token -> Token"
                    amount_in = "查看详情"

                swaps.append({
                    "hash": tx.get('hash', ''),
                    "type": swap_type,
                    "amount_in": amount_in,
                    "amount_out": "查看交易详情",
                    "time": time_str,
                    "from_token": "ETH" if value_eth > 0 else "Token",
                    "to_token": "Token"
                })

        return swaps


def trace_address_swaps_web(address: str, api_key: str = None) -> Dict[str, Any]:
    """Web interface for Uniswap tracing using Etherscan API.

    Args:
        address: ETH address to trace
        api_key: Etherscan API key (required for transaction history)

    Returns:
        Dict with success, address, swaps list, flow_diagram
    """
    # Validate address format
    if not validate_eth_address(address):
        return {
            "success": False,
            "error": "无效的ETH地址格式（需要0x开头的40位十六进制）",
            "address": address
        }

    # Require API key for transaction history
    if not api_key:
        return {
            "success": False,
            "error": "请提供Etherscan API密钥以查询交易历史",
            "address": address
        }

    try:
        tracker = UniswapTracker()
        swaps = tracker.get_address_transactions(address, api_key)

        return {
            "success": True,
            "address": Web3.to_checksum_address(address),
            "swaps": swaps,
            "swap_count": len(swaps),
            "flow_diagram": tracker.generate_flow_diagram(swaps)
        }

    except Exception as e:
        logger.error(f"Uniswap trace error: {e}")
        return {
            "success": False,
            "error": str(e),
            "address": address
        }


def get_eth_transactions(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """Get ETH transactions from Etherscan API.

    Args:
        address: ETH address
        api_key: Etherscan API key
        limit: Max transactions to fetch

    Returns:
        List of transaction dicts
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
        response = requests.get(ETHERSCAN_API_URL, params=params, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            return []

        data = response.json()
        if data.get('status') != '1':
            return []

        return data.get('result', [])
    except Exception as e:
        logger.error(f"Etherscan API error: {e}")
        return []