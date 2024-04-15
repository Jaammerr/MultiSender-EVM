from loader import config
from models import SocketContracts


CHAINS = [
    "Ethereum",
    "Optimism",
    "Arbitrium",
    "Binance Smart",
    "Polygon",
    "ZkSync Era",
    "Avalanche",
    "Base",
]

RPC_URLS = {
    "Ethereum": config.eth_rpc,
    "Optimism": config.op_rpc,
    "Arbitrium": config.arb_rpc,
    "Binance Smart": config.bsc_rpc,
    "Polygon": config.polygon_rpc,
    "ZkSync Era": config.zk_era_rpc,
    "Avalanche": config.avax_rpc,
    "Base": config.base_rpc,
}

CHAIN_IDS = {
    "Ethereum": 1,
    "Optimism": 10,
    "Arbitrium": 42161,
    "Binance Smart": 56,
    "Polygon": 137,
    "ZkSync Era": 324,
    "Avalanche": 43114,
    "Base": 8453,
}


CHAIN_SYMBOLS = {
    "Ethereum": "ETH",
    "Optimism": "ETH",
    "Arbitrium": "ETH",
    "Binance Smart": "BNB",
    "Polygon": "MATIC",
    "ZkSync Era": "ETH",
    "Avalanche": "AVAX",
    "Base": "ETH",
}


CHAIN_CONTRACTS = {
    "Ethereum": SocketContracts.eth,
    "Optimism": SocketContracts.op,
    "Arbitrium": SocketContracts.arb,
    "Binance Smart": SocketContracts.bsc,
    "Polygon": SocketContracts.polygon,
    "ZkSync Era": SocketContracts.zk_era,
    "Avalanche": SocketContracts.avax,
    "Base": SocketContracts.base,
}


CHAINS_EXPLORERS = {
    "Ethereum": "https://etherscan.io/tx/",
    "Optimism": "https://optimistic.etherscan.io/tx/",
    "Arbitrium": "https://arbiscan.io/tx/",
    "Binance Smart": "https://bscscan.com/tx/",
    "Polygon": "https://polygonscan.com/tx/",
    "ZkSync Era": "https://explorer.zksync.io/tx/",
    "Avalanche": "https://snowtrace.io/tx/",
    "Base": "https://basescan.org/tx/",
}
