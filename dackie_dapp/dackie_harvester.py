#!/usr/bin/python3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

from base_utils import get_contract_http, sign_tx, token_approve


header = {'Authorization': 'Bearer RvFMYEylf5IwLpAvy1T51JaKaO-aIHTyJ6jA4dWe5WUBAs88',
          'Content-Type': 'application/json'}
w3 = Web3(Web3.HTTPProvider('https://svc.blockdaemon.com/base/testnet/native/http-rpc',
                            request_kwargs={'headers': header}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Dackie Farms earn : Stake LP tokens to earn.
farms_addr = '0xDB8726189978d09D8c8A449Eda6c72A1e2EB228e'
farms_contract = get_contract_http(farms_addr)

def farms_stake(key: str, lp_adrr: str, pid: int):
    amount = token_approve(key, lp_adrr, farms_addr)
    account: LocalAccount = Account.from_key(key)
    tx_dict = farms_contract.functions.deposit(pid, amount).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'dackie farms stake')

def farms_harvest(key: str, pid=14):
    account: LocalAccount = Account.from_key(key)
    tx_dict = farms_contract.functions.deposit(pid, 0).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'dackie farms harvest')


# Dackie Pools earn : Just stake some tokens to earn.
dackie_token = '0xcf8E7e6b26F407dEE615fc4Db18Bf829E7Aa8C09'
pools_weth = '0x70249aF497f2040c0677f5Ea1B0dB2595f94803F'
pools_wbtc = '0xd2BC5Bd918779264aD08cfaC8A276dC6e96AF517'

def pools_stake(key: str, type='weth'):
    match type:
        case 'weth':
            spender = pools_weth
        case 'wbtc':
            spender = pools_wbtc
        case _:
            spender = pools_weth
    amount = token_approve(key, dackie_token, spender)
    pools_contract = get_contract_http(spender)
    account: LocalAccount = Account.from_key(key)
    tx_dict = pools_contract.functions.deposit(amount).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'dackie pools stake')

def pools_harvest(key: str, type='weth'):
    match type:
        case 'weth':
            pools_contract = get_contract_http(pools_weth)
        case 'wbtc':
            pools_contract = get_contract_http(pools_wbtc)
        case _:
            pools_contract = get_contract_http(pools_weth)
    account: LocalAccount = Account.from_key(key)
    tx_dict = pools_contract.functions.deposit(0).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'dackie pools harvest')
