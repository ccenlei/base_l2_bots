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


beagleswap_addr = '0xbe92671bdd1a1062E1A9F3Be618e399Fb5faCAcE'
beagleswap_contract = get_contract(beagleswap_addr, 'beagle_dapp/swap_abi.json')
weth_addr = '0x4200000000000000000000000000000000000006'
usdt_addr = '0x6440c59d7c7c108d3Bb90E4bDeeE8262c975858a'
usdc_addr = '0xB37A5498A6386b253FC30863A41175C3f9c0723B'
usd_addrs = (usdt_addr, usdc_addr)

def swap_eth2token(key: str, token_addr: str, amount=0.0121):
    account: LocalAccount = Account.from_key(key)
    path = [weth_addr, token_addr]
    to = account.address
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = beagleswap_contract.functions.swapExactETHForTokens(0, path, to, deadline).build_transaction(
        {
            'value': w3.to_wei(amount, 'ether'),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(to),
        })
    sign_tx(tx_dict, account, 'beagle swap eth for token')

def swap_token2eth(key: str, token_addr: str):
    account: LocalAccount = Account.from_key(key)
    addr = account.address
    token_balance = token_approve(key, token_addr, beagleswap_addr)
    path = [token_addr, weth_addr]
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = beagleswap_contract.functions.swapExactTokensForETH(
        token_balance, 0, path, addr, deadline).build_transaction(
        {
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(addr),
        })
    sign_tx(tx_dict, account, 'beagle swap token for eth')

def swap_token2token(key: str, token_ori_addr: str, token_tar_addr: str):
    account: LocalAccount = Account.from_key(key)
    addr = account.address
    token_balance = token_approve(key, token_ori_addr, beagleswap_addr)
    path = [token_ori_addr, token_tar_addr]
    deadline = int(datetime.now().timestamp()) + 1200
    tx_dict = beagleswap_contract.functions.swapExactTokensForTokens(
        token_balance, 0, path, addr, deadline).build_transaction(
        {
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(addr),
        })
    sign_tx(tx_dict, account, 'beagle swap token for token')
