#!/usr/bin/python3
import datetime
from apscheduler.schedulers.background import BlockingScheduler

from concurrent.futures import ThreadPoolExecutor
import json
import pymysql

from dapp_bots import dackie_bots,beagle_bots


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

# bot thread.
def dapp_bot(thread_id: int, name: str, key: str):
    print(f"start to bot dapp: id={thread_id}, name={name}")
    dackie_bots.bot_all(key)
    beagle_bots.bot_all(key)


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
        