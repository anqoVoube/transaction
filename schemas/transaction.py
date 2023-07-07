from pydantic import BaseModel, Field
from web3.types import Wei, Nonce


class Transaction(BaseModel):
    to: str
    value: Wei
    gas: int
    gas_price: Wei = Field(..., alias="gasPrice")
    nonce: Nonce
    chain_id: int = Field(80001, alias="chainId")
