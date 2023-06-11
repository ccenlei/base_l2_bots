#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import json

from dackie_dapp.dackie_harvester import dackie_harvest
from dackie_dapp.dackie_swapper import dackieswap_token2eth


# auto harvest dackie farms.
def automatic_dackie_harvest_bot(key: str):
    dackie_harvest(key)
    dackieswap_token2eth(key, '0xcf8E7e6b26F407dEE615fc4Db18Bf829E7Aa8C09')


# bot thread.
def dapp_bot(thread_id: int, name: str, key: str):
    print(f"start to bot: id={thread_id}, name={name}")
    automatic_dackie_harvest_bot(key)


if __name__ == '__main__':
    print('start to interact base l2 dapps.')
    file_path = 'accounts.json'
    with open(file_path, mode='r') as file:
        accounts = json.load(file)
    on_accounts = [account for account in accounts if account['is_on'] is True]
    index = 0
    with ThreadPoolExecutor(max_workers=10) as pool:
        for on_account in on_accounts:
            index += 1
            name, key = on_account['name'], on_account['key']
            thread = pool.submit(dapp_bot, index, name, key)
        