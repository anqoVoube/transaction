from abc import ABC, abstractmethod
from typing import Any

from hexbytes import HexBytes
from web3.main import BaseWeb3
from web3.types import Wei

from core.settings import settings
from schemas.transaction import Transaction
from utils.static import Static


class BaseSendCoinService(ABC):
    @abstractmethod
    def send(self) -> Any:
        ...


class SendCoin(BaseSendCoinService):
    def __init__(
        self,
        w3: BaseWeb3,
        value: Wei,
        gas: int,
        gas_price: Wei,
        private_key: str = settings.PRIVATE_KEY,
        receiver_address: str = settings.RECEIVER_ADDRESS,
        chain_id: int = 80001,
    ):
        self.w3 = w3
        self._private_key = private_key
        self.account_address = self.w3.eth.account.from_key(private_key).address

        # checks for valid amount of money being sent
        self.is_valid_send_amount(
            balance=w3.eth.get_balance(self.account_address),
            value=value
        )

        self.transaction_dict = Transaction(
            to=receiver_address,
            value=value,
            gas=gas,
            gasPrice=gas_price,
            nonce=w3.eth.get_transaction_count(self.account_address),
            chain_id=chain_id
        ).dict(by_alias=True)

    def send(self) -> HexBytes:
        signed_transaction = self.w3.eth.account.sign_transaction(self.transaction_dict, self._private_key)
        transaction_hash: HexBytes = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return transaction_hash

    @staticmethod
    def is_valid_send_amount(balance: Wei, value: Wei):  # This function can have bug, since we don't consider gas bills
        if balance < value:
            print(Static.INSUFFICIENT_BALANCE)
            return False
        return True

