#!/usr/bin/python3
import datetime
from apscheduler.schedulers.background import BlockingScheduler

from concurrent.futures import ThreadPoolExecutor
from base_utils import load_accs

from dapp_bots import dackie_bots,beagle_bots,cloud_bots


# db: from database; file: from accounts.json
acc_model = 'db'


# bot thread.
def dapp_bot(thread_id: int, name: str, key: str):
    print(f"start to bot dapp: id={thread_id}, name={name}")
    dackie_bots.bot_all(key)
    beagle_bots.bot_all(key)
    cloud_bots.bot_all(key)


def pool_excutes():
    print('start to interact base l2 dapps.')
    on_accounts = load_accs(acc_model)
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
        