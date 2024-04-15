from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    eth_rpc: HttpUrl
    op_rpc: HttpUrl
    bsc_rpc: HttpUrl
    polygon_rpc: HttpUrl
    zk_era_rpc: HttpUrl
    arb_rpc: HttpUrl
    avax_rpc: HttpUrl
    base_rpc: HttpUrl
    max_priority_fee_per_gas: float = 0.1
