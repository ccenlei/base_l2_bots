#!/usr/bin/python3
from cloud_dapp import cloud_harvester
from cloud_dapp import cloud_swapper


cloud_eth_lp = '0x377208A4697BaFb15438611D87617a5590E83817'
cloud_eth_lp_pid = 1


def __cloud_stake(key: str):
    cloud_harvester.farms_stake(key, cloud_eth_lp, cloud_eth_lp_pid)
    cloud_harvester.pool_stake(key)

def __cloud_harvest(key: str):
    cloud_harvester.farms_harvest(key, cloud_eth_lp_pid)
    cloud_harvester.pool_harvest(key)
    cloud_swapper.swap_token2eth(key, '0x8ae3d0E14Fe5BC0533a5Ca5e764604442d574a00')


def bot_all(key: str):
    __cloud_harvest(key)
