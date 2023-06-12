#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import json
import pymysql

from dackie_dapp.dackie_harvester import dackie_harvest
from dackie_dapp.dackie_swapper import dackieswap_token2eth
from oil_dapp.oil_harvester import oil_harvest


# db: from database; file: from accounts.json
acc_model = 'db'


def file_load_accs():
    file_path = 'accounts.json'
    with open(file_path, mode='r') as file:
        accounts = json.load(file)
        on_accounts = [account for account in accounts if account['is_on'] == 0]
    return on_accounts


def db_load_accs():
    with pymysql.connect(host='localhost', port=3306, user='ccenlei', password='123', database='web3') as db:
        cursor = db.cursor()
        sql = 'select name,address,pri_key from eth_account where is_on = 0'
        cursor.execute(sql)
        rows = cursor.fetchall()
        on_accounts = []
        for row in rows:
            acc_dic = {'name': row[0], 'addr': row[1], 'key': row[2]}
            on_accounts.append(acc_dic)
    return on_accounts


# auto harvest dackie farms.
def auto_dackie_harvest_bot(key: str):
    dackie_harvest(key)
    dackieswap_token2eth(key, '0xcf8E7e6b26F407dEE615fc4Db18Bf829E7Aa8C09')


nft_token_ids = (0,2)


# auto harvest oil farms.
def auto_oil_harvest_bot(key: str):
    for token_id in nft_token_ids:
        oil_harvest(key, token_id)
    dackieswap_token2eth(key, '0x5bC8BDC70D7cD2ff78E0CDA60d326685c047f7B5')



# bot thread.
def dapp_bot(thread_id: int, name: str, key: str):
    print(f"start to bot: id={thread_id}, name={name}")
    auto_dackie_harvest_bot(key)
    auto_oil_harvest_bot(key)


if __name__ == '__main__':
    print('start to interact base l2 dapps.')
    match acc_model:
        case 'db':
            on_accounts = db_load_accs()
        case 'file':
            on_accounts = file_load_accs()
        case _:
            print('select a way of accounts load.')
            exit(-1)
    index = 0
    with ThreadPoolExecutor(max_workers=10) as pool:
        for on_account in on_accounts:
            index += 1
            name, key = on_account['name'], on_account['key']
            thread = pool.submit(dapp_bot, index, name, key)
        