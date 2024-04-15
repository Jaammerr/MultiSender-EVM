from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class SocketContracts:
    eth: str = "0xb584d4be1a5470ca1a8778e9b86c81e165204599"
    op: str = "0x5800249621da520adfdca16da20d8a5fc0f814d8"
    bsc: str = "0xBE51D38547992293c89CC589105784ab60b004A9"
    gno: str = "0xBE51D38547992293c89CC589105784ab60b004A9"
    polygon: str = "0xAC313d7491910516E06FBfC2A0b5BB49bb072D91"
    zk_era: str = "0xaDdE7028e7ec226777e5dea5D53F6457C21ec7D6"
    arb: str = "0xc0e02aa55d10e38855e13b64a8e1387a04681a00"
    avax: str = "0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB"
    aur: str = "0x2b42AFFD4b7C14d9B7C2579229495c052672Ccd3"
    ftm: str = "0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB"
    base: str = "0xE8c5b8488FeaFB5df316Be73EdE3Bdc26571a773"
    abi: list = open("./abi/socket.json", "r").read()


class Fees(BaseModel):
    max_priority_fee_per_gas: int
    max_fee_per_gas: int
