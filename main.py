from typing import Tuple, Any

from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
from web3.main import BaseWeb3
from web3.types import Wei

from core.settings import settings
from services.send import SendCoin
from utils.static import Static


def send_transaction(
        w3: BaseWeb3,
        value: Tuple[Any, str],
        gas: int,
        gas_price: Tuple[Any, str]
):
    wei_value: Wei = w3.to_wei(*value)
    wei_gas_price: Wei = w3.to_wei(*gas_price)

    send_coin_service = SendCoin(
        w3=w3,
        value=wei_value,
        gas=gas,
        gas_price=wei_gas_price
    )

    transaction_hash: HexBytes = send_coin_service.send()
    print(transaction_hash)
    print(f"Transaction is: {transaction_hash.hex()}")


if __name__ == "__main__":
    send_transaction(
        Web3(HTTPProvider(settings.PROVIDER_URL)),
        value=(0.333, Static.ETHER),
        gas=21000,
        gas_price=(1, Static.GWEI)
    )
