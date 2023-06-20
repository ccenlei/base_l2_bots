#!/usr/bin/python3
from beagle_dapp import beagle_harvester
from beagle_dapp import beagle_swapper


pids = (3,)


def __farms_bot(key: str):
    for pid in pids:
        beagle_harvester.farms_harvest(key, pid)
    beagle_swapper.swap_token2eth(key, '0x58388CF6220DF8c113BfB087617055E23c19067f')


def bot_all(key: str):
    __farms_bot(key)
