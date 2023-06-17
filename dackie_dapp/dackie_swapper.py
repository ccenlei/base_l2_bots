#!/usr/bin/python3
from datetime import datetime
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

from base_utils import get_contract, sign_tx, token_approve


header = {'Authorization': 'Bearer RvFMYEylf5IwLpAvy1T51JaKaO-aIHTyJ6jA4dWe5WUBAs88',
          'Content-Type': 'application/json'}
w3 = Web3(Web3.HTTPProvider('https://svc.blockdaemon.com/base/testnet/native/http-rpc',
                            request_kwargs={'headers': header}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
dackieswap_contract_addr = '0x29843613c7211D014F5Dd5718cF32BCD314914CB'


dackieswap_contract = get_contract(dackieswap_contract_addr, 'dackie_dapp/swap_abi.json')

def dackieswap_eth2token(key: str, token_addr: str, amount=0.0121):
    account: LocalAccount = Account.from_key(key)
    path = ['==weth addr==', token_addr]
    to = account.address
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = dackieswap_contract.functions.swapExactETHForTokens(0, path, to, deadline).build_transaction(
        {
            'value': w3.to_wei(amount, 'ether'),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(to),
        })
    sign_tx(tx_dict, account, 'dackie swap eth for token')

def dackieswap_token2eth(key: str, token_addr: str):
    account: LocalAccount = Account.from_key(key)
    addr = account.address
    token_balance = token_approve(key, token_addr)
    weth_addr = '0x4200000000000000000000000000000000000006'
    path = [token_addr, weth_addr]
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = dackieswap_contract.functions.swapExactTokensForETH(
        token_balance, 0, path, addr, deadline).build_transaction(
        {
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(addr),
        })
    sign_tx(tx_dict, account, 'dackie swap token for eth')

def dackieswap_token2token(key: str, token_ori_addr: str, token_tar_addr: str):
    account: LocalAccount = Account.from_key(key)
    addr = account.address
    token_balance = token_approve(key, token_ori_addr)
    path = [token_ori_addr, '==weth addr==', token_tar_addr]
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = dackieswap_contract.functions.swapExactTokensForTokens(
        token_balance, 0, path, addr, deadline).build_transaction(
        {
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(addr),
        })
    sign_tx(tx_dict, account, 'dackie swap token for token')
