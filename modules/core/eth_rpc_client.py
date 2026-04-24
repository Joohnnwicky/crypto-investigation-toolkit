"""Web3 RPC client for Ethereum blockchain queries with retry logic"""

import logging
import time
from typing import Optional

try:
    from web3 import Web3, HTTPProvider
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    Web3 = None
    HTTPProvider = None

# ETH RPC endpoints (per D-01)
ETH_RPC_PRIMARY = "https://eth.drpc.org"
ETH_RPC_FALLBACK = "https://eth.llamarpc.com"

# Configure logging
logger = logging.getLogger(__name__)


class EthRpcClient:
    """Web3 RPC client with retry logic and fallback node support.

    Used for Ethereum blockchain queries (Uniswap, Tornado Cash tracing).
    Implements retry logic (3 retries, 5-second timeout) per RESEARCH.md.
    """

    def __init__(self, rpc_url: Optional[str] = None, max_retries: int = 3, timeout: int = 5):
        """Initialize RPC client.

        Args:
            rpc_url: Custom RPC URL (optional, defaults to primary)
            max_retries: Number of retry attempts (default 3)
            timeout: Request timeout in seconds (default 5)
        """
        if not WEB3_AVAILABLE:
            raise ImportError("web3 library not installed. Run: pip install web3==7.15.0")

        self.rpc_url = rpc_url or ETH_RPC_PRIMARY
        self.max_retries = max_retries
        self.timeout = timeout
        self._w3: Optional[Web3] = None
        self._connected = False

    def get_web3(self) -> Web3:
        """Get connected Web3 instance with retry logic.

        Attempts connection with retry and fallback to backup node.

        Returns:
            Connected Web3 instance

        Raises:
            ConnectionError: If all connection attempts fail
        """
        if self._w3 and self._connected:
            return self._w3

        # Try primary node
        self._w3 = self._try_connect(self.rpc_url)
        if self._w3 and self._w3.is_connected():
            self._connected = True
            logger.info(f"Connected to ETH RPC: {self.rpc_url}")
            return self._w3

        # Try fallback node
        logger.warning(f"Primary node {self.rpc_url} failed, trying fallback")
        self._w3 = self._try_connect(ETH_RPC_FALLBACK)
        if self._w3 and self._w3.is_connected():
            self._connected = True
            logger.info(f"Connected to ETH RPC fallback: {ETH_RPC_FALLBACK}")
            return self._w3

        raise ConnectionError("Failed to connect to any ETH RPC node")

    def _try_connect(self, url: str) -> Optional[Web3]:
        """Attempt connection with retry logic.

        Args:
            url: RPC URL to try

        Returns:
            Web3 instance if successful, None otherwise
        """
        for attempt in range(self.max_retries):
            try:
                w3 = Web3(HTTPProvider(url, request_kwargs={'timeout': self.timeout}))
                if w3.is_connected():
                    return w3
                logger.warning(f"Connection attempt {attempt + 1} failed for {url}")
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} error for {url}: {e}")

            if attempt < self.max_retries - 1:
                time.sleep(1)  # Brief pause before retry

        return None

    def is_connected(self) -> bool:
        """Check if client is connected to RPC node.

        Returns:
            True if connected, False otherwise
        """
        return self._connected and self._w3 is not None and self._w3.is_connected()

    def get_block_number(self) -> int:
        """Get current block number.

        Returns:
            Current block number

        Raises:
            ConnectionError: If not connected
        """
        w3 = self.get_web3()
        return w3.eth.block_number