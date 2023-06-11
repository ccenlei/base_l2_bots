#!/usr/bin/python3
from collections.abc import Callable, Iterable, Mapping
import json
import random
import threading
from typing import Any, Union, Type

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/9f12bfa9c9d94a99abb9198de4f97587'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def get_abi(path: str):
    with open(path, mode='r') as file:
        data = json.load(file)
        contract_abi = data['result']
    return contract_abi


def get_contract(contract_addr: str, abi_path: str):
    addr = Web3.to_checksum_address(contract_addr)
    contract = w3.eth.contract(address=addr, abi=get_abi(abi_path))
    return contract


class BridgerAccount(threading.Thread):
    def __init__(self, thread_id: int, name: str, key: str, addr: str, l2_value: int,
                 contract: Union[Type[Contract], Contract]) -> None:
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.key = key
        self.addr = addr
        self.l2_value = l2_value
        self.contract = contract

    def run(self) -> None:
        print(f"start to bridge: id={self.thread_id}, name={self.name}")
        account: LocalAccount = Account.from_key(self.key)
        value = self.l2_value + 800000000000000
        tx_dict = self.contract.functions.requestL2Transaction(
            self.addr, self.l2_value, bytes(0), 742563, 800, [], self.addr
        ).build_transaction({
            'value': value,
            'gas': 150000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
        signed_tx = account.sign_transaction(transaction_dict=tx_dict)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"id={self.thread_id}, name={self.name} ==> tx_hash : {tx_hash.hex()}, status: {tx_receipt['status']}")


def bridger_base():
    l2_value = Web3.to_wei(0.21, 'ether')
    bridger_contract = get_contract('=============real contract addr===============', 'bridger_abi.json')
    with open('accounts.json', mode='r') as file:
        accounts = json.load(file)
    on_accounts = [account for account in accounts if account['is_on'] is True]
    random.shuffle(on_accounts)
    index = 0
    for on_account in on_accounts:
        index += 1
        name, key, addr = on_account['name'], on_account['key'], on_account['addr']
        thread = BridgerAccount(index, name, key, addr, l2_value, bridger_contract)
        thread.start()
        thread.join()


bridger_base()
