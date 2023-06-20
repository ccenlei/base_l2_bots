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


# ====================================Cloud Farms earn : Stake LP tokens to earn.====================================
farms_addr = '0x0c6F2bCD7d53829afa422b4535c8892B1566E8c5'
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
    sign_tx(tx_dict, account, 'cloud farms stake')

def farms_harvest(key: str, pid=1):
    account: LocalAccount = Account.from_key(key)
    tx_dict = farms_contract.functions.deposit(pid, 0).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'cloud farms harvest')
# ====================================Cloud Farms earn : Stake LP tokens to earn.====================================


# ====================================Cloud Pools earn : Just stake some tokens to earn.====================================
cloud_token = '0x8ae3d0E14Fe5BC0533a5Ca5e764604442d574a00'
pool_addr = '0x3b28a70a60253deC8056b6f4328E9B630dB09181'
pool_contract = get_contract_http(pool_addr)

def pool_stake(key: str):
    amount = token_approve(key, cloud_token, pool_addr)
    account: LocalAccount = Account.from_key(key)
    tx_dict = pool_contract.functions.deposit(amount).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'cloud pools stake')

def pool_harvest(key: str):
    account: LocalAccount = Account.from_key(key)
    tx_dict = pool_contract.functions.deposit(0).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'cloud pools harvest')
# ====================================Cloud Pools earn : Just stake some tokens to earn.====================================
