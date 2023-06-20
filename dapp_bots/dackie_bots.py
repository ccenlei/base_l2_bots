#!/usr/bin/python3
from dackie_dapp import dackie_harvester
from dackie_dapp import dackie_swapper


pids = (17,)
types = ('weth',)


def __farms_bot(key: str):
    for pid in pids:
        dackie_harvester.farms_harvest(key, pid)
    dackie_swapper.swap_token2eth(key, '0xcf8E7e6b26F407dEE615fc4Db18Bf829E7Aa8C09')

def __pools_bot(key: str):
    for type in types:
       dackie_harvester.pools_harvest(key, type)


def bot_all(key: str):
    __farms_bot(key)
    __pools_bot(key)