#!/usr/bin/python3
import json
import requests
import pymysql

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3


def get_contract(contract_addr: str, abi_path: str, w3: Web3):
    addr = Web3.to_checksum_address(contract_addr)
    with open(abi_path, mode='r') as file:
        data = json.load(file)
        contract_abi = data['result']
    contract = w3.eth.contract(address=addr, abi=contract_abi)
    return contract


def get_contract_http(contract_addr: str, w3: Web3):
    abi_endpoint = f'https://api-goerli.basescan.org/api?module=contract&action=getabi&address={contract_addr}'
    with requests.get(abi_endpoint) as response:
        response_json = response.json()
        contract_abi = json.loads(response_json['result'])
    contract = w3.eth.contract(address=contract_addr, abi=contract_abi)
    return contract


def sign_tx(tx_dict: dict, account: LocalAccount, w3: Web3, lefix: str):
    signed_tx = account.sign_transaction(transaction_dict=tx_dict)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"{lefix} : {account.address} ==> tx_hash : {tx_hash.hex()}, status: {tx_receipt['status']}")


def token_approve(key: str, token_addr: str, spender_addr: str, w3: Web3, token_abi=''):
    account: LocalAccount = Account.from_key(key)
    addr = account.address
    if '' == token_abi:
        token_contract = get_contract_http(token_addr, w3)
    else:
        token_contract = get_contract(token_addr, token_abi, w3)
    token_balance = token_contract.functions.balanceOf(addr).call()
    spender, amount = spender_addr, token_balance
    tx_dict = token_contract.functions.approve(spender, amount).build_transaction(
        {
            'value': 0,
            'gas': 55000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(addr),
        })
    sign_tx(tx_dict, account, w3, 'token approve')
    return token_balance


def file_load_accs():
    file_path = 'accounts.json'
    with open(file_path, mode='r') as file:
        accounts = json.load(file)
        on_accounts = [account for account in accounts if account['is_on'] == 0]
    return on_accounts


def db_load_accs():
    with pymysql.connect(host='localhost', port=3306, user='ccenlei', password='123', database='web3') as db:
        cursor = db.cursor()
        sql = 'select name,address,pri_key from eth_account where is_on = 0'
        cursor.execute(sql)
        rows = cursor.fetchall()
        on_accounts = []
        for row in rows:
            acc_dic = {'name': row[0], 'addr': row[1], 'key': row[2]}
            on_accounts.append(acc_dic)
    return on_accounts


def load_accs(model: str):
     match model:
        case 'db':
            return db_load_accs()
        case 'file':
            return file_load_accs()
        case _:
            print('select a way of accounts load.')
            exit(-1)
