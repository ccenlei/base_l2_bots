#!/usr/bin/python3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

from base_utils import get_contract, sign_tx, load_accs


infura_key = '9f12bfa9c9d94a99abb9198de4f97587'
w3 = Web3(Web3.HTTPProvider(f'https://goerli.infura.io/v3/{infura_key}'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# db: from database; file: from accounts.json
acc_model = 'db'
l2_value = Web3.to_wei(0.21, 'ether')

bridge_addr = '0xe93c8cD0D409341205A592f8c4Ac1A5fe5585cfA'
bridge_contract = get_contract(bridge_addr, 'bridge_abi.json', w3)


def bridge_account(key: str, addr: str):
    account: LocalAccount = Account.from_key(key)
    tx_dict = bridge_contract.functions.depositTransaction(
        addr, l2_value, 100000, False, bytes(0)
    ).build_transaction({
        'value': l2_value,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
    })
    sign_tx(tx_dict, account, w3, 'base bridge')

def bridge_base():
    accounts = load_accs(acc_model)
    for account in accounts:
        name, key, addr = account['name'], account['key'], account['addr']
        print(f'start to bridge account : {name}')
        bridge_account(key, addr)


bridge_base()
