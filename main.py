#!/usr/bin/python3
import datetime
from apscheduler.schedulers.background import BlockingScheduler

from concurrent.futures import ThreadPoolExecutor
import json
import pymysql

from dackie_dapp import dackie_harvester,dackie_swapper
from beagle_dapp import beagle_harvester,beagle_swapper
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


# ====================================auto harvest dackie.====================================
def dackie_farms_bot(key: str):
    dackie_pids = (17,)
    for pid in dackie_pids:
        dackie_harvester.farms_harvest(key, pid)
    dackie_swapper.swap_token2eth(key, '0xcf8E7e6b26F407dEE615fc4Db18Bf829E7Aa8C09')

def dackie_pools_bot(key: str):
    dackie_types = ('weth',)
    for type in dackie_types:
        dackie_harvester.pools_harvest(key, type)
# ====================================auto harvest dackie.====================================


# ====================================auto harvest beagle.====================================
def beagle_farms_bot(key: str):
    beagle_pids = (3,)
    for pid in beagle_pids:
        beagle_harvester.farms_harvest(key, pid)
    beagle_swapper.swap_token2eth(key, '0x58388CF6220DF8c113BfB087617055E23c19067f')
# ====================================auto harvest beagle.====================================


# ====================================auto harvest oil farms.====================================
def oil_harvest_bot(key: str):
    for token_id in oil_token_ids:
        oil_token_ids = (0,2)
        oil_harvest(key, token_id)
    dackie_swapper.swap_token2eth(key, '0x5bC8BDC70D7cD2ff78E0CDA60d326685c047f7B5')
# ====================================auto harvest dackie.====================================


# bot thread.
def dapp_bot(thread_id: int, name: str, key: str):
    print(f"start to bot: id={thread_id}, name={name}")
    dackie_farms_bot(key)
    dackie_pools_bot(key)
    beagle_farms_bot(key)
    # oil_harvest_bot(key)


def pool_excutes():
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


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # minutes seconds
    scheduler.add_job(pool_excutes, 'interval', minutes=36, next_run_time=datetime.datetime.now())
    scheduler.start()
        