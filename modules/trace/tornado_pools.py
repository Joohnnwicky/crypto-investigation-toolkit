"""Tornado Cash pool addresses and event ABIs configuration"""

# Tornado Cash mixer pool addresses
# V1 pools (legacy, may be deprecated)
TORNADO_POOLS = {
    "0.1 ETH": "0x12D66f87A04A9E220743712cE6d9bB1B5616B8Fc",
    "1 ETH": "0x910Cbd523D972eb0a6f4cAe4618aD9491718b368",
    "10 ETH": "0xA160CdAB225685dA1d56d342E7850264303fed3",
    "100 ETH": "0xD4B88Df4D29F5CedD6857912842cff3b20C8C0fd",
    # V2 pools (post-2022)
    "1 ETH V2": "0x84443CFd09A48AF6eF359CCEc6554bB16f6614B1",
    "10 ETH V2": "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
}

# Pool metadata
POOL_INFO = {
    "0.1 ETH": {"amount": 0.1, "version": "V1"},
    "1 ETH": {"amount": 1.0, "version": "V1"},
    "10 ETH": {"amount": 10.0, "version": "V1"},
    "100 ETH": {"amount": 100.0, "version": "V1"},
    "1 ETH V2": {"amount": 1.0, "version": "V2"},
    "10 ETH V2": {"amount": 10.0, "version": "V2"},
}

# Withdrawal event ABI (from canonical script lines 42-52)
WITHDRAWAL_EVENT_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "relayer", "type": "address"},
        {"indexed": True, "name": "recipient", "type": "address"},
        {"indexed": False, "name": "fee", "type": "uint256"},
        {"indexed": False, "name": "timestamp", "type": "uint256"}
    ],
    "name": "Withdrawal",
    "type": "event"
}

# Deposit event ABI (from canonical script lines 33-41)
DEPOSIT_EVENT_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "leaf", "type": "bytes32"},
        {"indexed": False, "name": "timestamp", "type": "uint256"}
    ],
    "name": "Deposit",
    "type": "event"
}

# Known exchange address prefixes (for confidence scoring)
EXCHANGE_PREFIXES = {
    "0xa9b1": "Coinbase",
    "0x3b5d": "Coinbase",
    "0x28c6": "Binance",
    "0xfbb1": "Binance",
    "0x2910": "Kraken",
    "0x503d": "OKX",
}