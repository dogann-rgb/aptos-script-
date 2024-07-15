import os
import sys

project_path = os.path.abspath(os.path.dirname(__file__))


aptos_sdk_path = '/Users/ozgurdogan/Desktop/wecando/slippage/venv/lib/python3.12/site-packages'
sys.path.append(aptos_sdk_path)



import random
import time
from aptos_sdk.account import Account
from config import node_url, tokens_mapping, slippage_tolerance, show_balance_before_swap, show_balance_after_swap, randomize_wallets, is_sleep, sleep_from, sleep_to
from liquidswap.client import LiquidSwapClient

from liquidswap.constants import COIN_INFO


wallet_private_key = 'private key'
account = Account.load_key(wallet_private_key)

# LiquidSwap Client Oluşturma
liquidswap_client = LiquidSwapClient(node_url)

# Ana fonksiyon
def main():
    from_token = 'APT'
    amount = 10
    to_contract = 'target contract address'

    if show_balance_before_swap:
        balance_before = liquidswap_client.get_balance(account, from_token)
        print(f"Swap öncesi {from_token} bakiyesi: {balance_before}")

    min_amount_out = liquidswap_client.calculate_min_amount_out(amount, slippage_tolerance)

    result = liquidswap_client.buy_coin_by_contract(account, from_token, to_contract, amount, min_amount_out)
    if result:
        print(f"Token başarıyla satın alındı: {result}")
    else:
        print("Token satın alınırken hata oluştu")

    if show_balance_after_swap:
        balance_after = liquidswap_client.get_balance(account, from_token)
        print(f"Swap sonrası {from_token} bakiyesi: {balance_after}")

    if is_sleep:
        sleep_time = random.randint(sleep_from, sleep_to)
        print(f"{sleep_time} saniye bekleniyor...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
