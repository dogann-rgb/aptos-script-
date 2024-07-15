from typing import Union
from loguru import logger
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk import ed25519
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from aptos_sdk.type_tag import StructTag, TypeTag

from ..constants import COIN_INFO, NETWORKS_MODULES, RESOURCES_ACCOUNT, FEE_SCALE, FEE_PCT, CURVES

class LiquidSwapClient:
    def __init__(self, node_url: str):
        self.node_url = node_url
        self.rest_client = RestClient(node_url)

    def get_new_coins(self):
        response = requests.get(f"{self.node_url}/new-coins")
        if response.status_code == 200:
            return response.json()['new_coins']
        else:
            logger.error("Yeni coinleri tespit ederken hata oluştu: {}", response.text)
            return []

    def buy_coin_by_contract(self, account: Account, from_token: str, to_contract: str, amount: int, min_amount_out: int):
        payload = EntryFunction.natural(
            "0x1::Coin",
            "swap",
            [],
            [
                TransactionArgument.from_string(COIN_INFO[from_token]),
                TransactionArgument.from_address(to_contract),
                TransactionArgument.from_u64(amount),
                TransactionArgument.from_u64(min_amount_out)
            ]
        )
        txn = self.rest_client.create_transaction(account.address(), payload)
        signed_txn = account.sign(txn)
        result = self.rest_client.submit(signed_txn)
        return result

    def get_balance(self, account: Account, token_type: str):
        resources = self.rest_client.account_resources(account.address())
        for resource in resources:
            if resource["type"] == f"0x1::Coin::CoinStore<{COIN_INFO[token_type]}>":
                return int(resource["data"]["coin"]["value"])
        return 0

    def calculate_min_amount_out(self, amount: int, slippage_tolerance: float) -> int:
        min_amount_out = amount * (1 - (slippage_tolerance / 100))
        return int(min_amount_out)
