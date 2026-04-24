"""Tornado Cash mixer tracing module with time window analysis"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    Web3 = None

from modules.core.eth_rpc_client import EthRpcClient
from .tornado_pools import TORNADO_POOLS, WITHDRAWAL_EVENT_ABI, EXCHANGE_PREFIXES

# Configure logging
logger = logging.getLogger(__name__)

# Time window configuration (per D-07)
DEFAULT_WINDOW_HOURS = 24

# Ethereum genesis block timestamp
ETH_GENESIS_TS = datetime(2015, 7, 30, 15, 26, 28).timestamp()
ETH_AVG_BLOCK_TIME = 12  # Average 12 seconds per block


def validate_deposit_time(deposit_time: str) -> bool:
    """Validate deposit time format.

    Args:
        deposit_time: Time string

    Returns:
        True if format is YYYY-MM-DD HH:MM:SS
    """
    if not deposit_time:
        return False
    return bool(re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', deposit_time))


class TornadoCashTracker:
    """Tornado Cash mixer withdrawal tracker with time window analysis."""

    def __init__(self):
        """Initialize tracker with EthRpcClient."""
        self.rpc_client = EthRpcClient()
        self.w3: Optional[Web3] = None

    def _get_w3(self) -> Web3:
        """Get Web3 instance."""
        if self.w3 is None:
            self.w3 = self.rpc_client.get_web3()
        return self.w3

    def _block_from_timestamp(self, timestamp: float) -> int:
        """Estimate block number from timestamp.

        Args:
            timestamp: Unix timestamp

        Returns:
            Estimated block number
        """
        return int((timestamp - ETH_GENESIS_TS) / ETH_AVG_BLOCK_TIME)

    def get_withdrawals(self, pool_address: str, start_block: int, end_block: int) -> List[Dict]:
        """Get withdrawal events from pool using get_logs.

        Note: Public RPC nodes don't support create_filter, must use get_logs.

        Args:
            pool_address: Pool contract address
            start_block: Starting block number
            end_block: Ending block number

        Returns:
            List of withdrawal events
        """
        try:
            w3 = self._get_w3()

            contract = w3.eth.contract(
                address=Web3.to_checksum_address(pool_address),
                abi=[WITHDRAWAL_EVENT_ABI]
            )

            # Use get_logs (not create_filter) per RESEARCH.md
            withdrawals = contract.events.Withdrawal.get_logs(
                from_block=max(0, start_block),
                to_block=min(end_block, w3.eth.block_number)
            )

            result = []
            for wd in withdrawals:
                try:
                    result.append({
                        "block_number": wd.blockNumber,
                        "transaction_hash": wd.transactionHash.hex(),
                        "relayer": wd.args.relayer,
                        "recipient": wd.args.recipient,
                        "fee": float(w3.from_wei(wd.args.fee, 'ether')),
                        "timestamp": wd.args.timestamp,
                        "date": datetime.fromtimestamp(wd.args.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse withdrawal event: {e}")

            return result

        except Exception as e:
            logger.error(f"Failed to get withdrawals from {pool_address}: {e}")
            return []

    def identify_exchange(self, address: str) -> Optional[str]:
        """Identify if address belongs to known exchange.

        Args:
            address: ETH address

        Returns:
            Exchange name or None
        """
        prefix = address[:6].lower()
        return EXCHANGE_PREFIXES.get(prefix)

    def calculate_confidence(self, withdrawal: Dict, deposit_ts: float) -> tuple:
        """Calculate confidence level for withdrawal.

        Args:
            withdrawal: Withdrawal event dict
            deposit_ts: Deposit timestamp

        Returns:
            (confidence, reason) tuple
        """
        # Check if withdrawal goes to exchange
        exchange = self.identify_exchange(withdrawal['recipient'])
        if exchange:
            return "HIGH", f"立即转入{exchange}交易所，高度可疑"

        # Check withdrawal timing
        withdraw_ts = withdrawal['timestamp']
        hours_diff = (withdraw_ts - deposit_ts) / 3600

        if hours_diff < 6:
            return "MEDIUM", f"存款后 {hours_diff:.1f} 小时即提款，较可疑"
        elif hours_diff < 24:
            return "LOW", f"存款后 {hours_diff:.1f} 小时提款"

        return "LOW", "时间窗口边缘提款"

    def search_all_pools(self, deposit_time: str, window_hours: int = DEFAULT_WINDOW_HOURS) -> List[Dict]:
        """Search all Tornado pools for suspicious withdrawals.

        Args:
            deposit_time: Deposit time string (YYYY-MM-DD HH:MM:SS)
            window_hours: Time window in hours (default 24 per D-07)

        Returns:
            List of suspicious withdrawals with confidence levels
        """
        # Parse deposit time
        try:
            deposit_ts = datetime.strptime(deposit_time, "%Y-%m-%d %H:%M:%S").timestamp()
        except ValueError:
            return []

        # Calculate block range
        start_ts = deposit_ts
        end_ts = deposit_ts + (window_hours * 3600)

        start_block = self._block_from_timestamp(start_ts)
        end_block = self._block_from_timestamp(end_ts)

        suspicious_withdrawals = []

        # Search all pools (per D-11: auto-search all pools)
        for pool_name, pool_address in TORNADO_POOLS.items():
            withdrawals = self.get_withdrawals(pool_address, start_block, end_block)

            for wd in withdrawals:
                wd_ts = wd['timestamp']

                # Check if within time window
                if start_ts <= wd_ts <= end_ts:
                    confidence, reason = self.calculate_confidence(wd, deposit_ts)

                    suspicious_withdrawals.append({
                        "pool": pool_name,
                        "recipient": wd['recipient'],
                        "fee": wd['fee'],
                        "date": wd['date'],
                        "tx_hash": wd['transaction_hash'],
                        "confidence": confidence,
                        "reason": reason
                    })

        return suspicious_withdrawals

    def generate_flow_diagram(self, deposit_time: str, withdrawals: List[Dict]) -> str:
        """Generate ASCII flow diagram for mixer tracing.

        Args:
            deposit_time: Deposit time string
            withdrawals: List of suspicious withdrawals

        Returns:
            ASCII diagram string
        """
        diagram = f"""
┌─────────────────────────────────────────────────────────────┐
│  混币器追踪流程                                               │
├─────────────────────────────────────────────────────────────┤
│  存款时间: {deposit_time}                                     │
│  时间窗口: {DEFAULT_WINDOW_HOURS}小时                         │
│  可疑提款: {len(withdrawals)} 笔                              │
│                                                              │
│  [Tornado Cash Pool] → [提款地址] → 置信度                    │
│                                                              │"""

        for wd in withdrawals[:5]:  # Show top 5
            diagram += f"""
│  [{wd['pool']}] → [{wd['recipient'][:12]}...] → {wd['confidence']}"""

        diagram += """
└─────────────────────────────────────────────────────────────┘
"""
        return diagram


def time_window_analysis_web(deposit_time: str) -> Dict[str, Any]:
    """Web interface for mixer tracing.

    Args:
        deposit_time: Deposit time string "YYYY-MM-DD HH:MM:SS"

    Returns:
        Dict with success, deposit_time, suspicious_withdrawals, flow_diagram
    """
    # Validate deposit time format
    if not validate_deposit_time(deposit_time):
        return {
            "success": False,
            "error": "无效的存款时间格式，请使用 YYYY-MM-DD HH:MM:SS 格式",
            "deposit_time": deposit_time
        }

    try:
        tracker = TornadoCashTracker()
        suspicious_withdrawals = tracker.search_all_pools(deposit_time)

        # Sort by confidence (HIGH first)
        suspicious_withdrawals.sort(key=lambda x: (
            0 if x['confidence'] == 'HIGH' else
            1 if x['confidence'] == 'MEDIUM' else 2
        ))

        return {
            "success": True,
            "deposit_time": deposit_time,
            "window_hours": DEFAULT_WINDOW_HOURS,
            "suspicious_withdrawals": suspicious_withdrawals,
            "flow_diagram": tracker.generate_flow_diagram(deposit_time, suspicious_withdrawals)
        }

    except Exception as e:
        logger.error(f"Mixer trace error: {e}")
        return {
            "success": False,
            "error": str(e),
            "deposit_time": deposit_time
        }