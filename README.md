# Bungee MultiSender via Socket
<img src="/console/images/img.png" alt="Alt text" title="Optional title">

## 🔗 Links

🔔 CHANNEL: https://t.me/JamBitPY

💬 CHAT: https://t.me/JamBitChat

💰 DONATION EVM ADDRESS: 0x08e3fdbb830ee591c0533C5E58f937D312b07198

## 📝 Description
``` This script allows you to send stablecoins to multiple addresses from your main wallet. The main advantage is that the sending occurs through the Bungee Socket contract, so the transaction fee will be minimal and it is impossible to find out the original address of the sender. ```

Supported sub-accounts format:

```You will be able to drop TXT with accounts while working with the console```
- address (static amount)
- address, amount (dynamic amount)

Supported networks:
- Binance Smart Chain
- Ethereum
- Polygon
- Avalanche
- Arbitrium
- Optimism
- Base
- ZkSync Era


## 📦 Installation
```bash
git clone this repository and open CMD in the folder
install the required packages: pip install -r requirements.txt
start the script: python run.py
```


## ⚙️ Config (config > settings.yaml)

```It is highly recommended to use your own RPCs via https://www.ankr.com/```

| Name    | Description                                                 |
|---------|-------------------------------------------------------------|
| eth_rpc | ETH RPC URL (if not have, leave the default value)          |
| op_rpc  | OPTIMISM RPC URL (if not have, leave the default value)     |
| bsc_rpc | Binance Smart RPC URL(if not have, leave the default value) |
| polygon_rpc | POLYGON RPC URL (if not have, leave the default value)      |
| zk_era_rpc | ZKSYNC ERA RPC URL(if not have, leave the default value)    |
| avax_rpc | AVALANCHE RPC URL (if not have, leave the default value)    |
| base_rpc | BASE RPC URL (if not have, leave the default value)         |


## 📄 Results
```After the script is completed, you will be able to see txt files with success/failed wallets in the <<results>> folder```
