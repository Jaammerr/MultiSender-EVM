from pydantic import BaseModel


class Account(BaseModel):
    address: str
    amount: float


class AccountsData(BaseModel):
    source_chain: str = "Ethereum"
    destination_chain: str = "Optimism"
    max_priority_fee_per_gas: float = 0.05
    bridge_amount: float = 0
    private_key: str = ""
    mnemonic: str = ""
    addresses: list[Account] = []
