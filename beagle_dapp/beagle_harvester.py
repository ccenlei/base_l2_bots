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


# ====================================Beagle Farms earn : Stake LP tokens to earn.====================================
farms_addr = '0x9C482dA80BcB146D588aE0F13650b2E84D5F709E'
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
    sign_tx(tx_dict, account, 'beagle farms stake')

def farms_harvest(key: str, pid=14):
    account: LocalAccount = Account.from_key(key)
    tx_dict = farms_contract.functions.deposit(pid, 0).build_transaction(
        {
            'value': 0,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account, 'beagle farms harvest')
# ====================================Beagle Farms earn : Stake LP tokens to earn.====================================
