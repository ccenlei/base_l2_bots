#!/usr/bin/python3
import json
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware


header = {'Authorization': 'Bearer RvFMYEylf5IwLpAvy1T51JaKaO-aIHTyJ6jA4dWe5WUBAs88',
          'Content-Type': 'application/json'}
w3 = Web3(Web3.HTTPProvider('https://svc.blockdaemon.com/base/testnet/native/http-rpc',
                            request_kwargs={'headers': header}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def get_contract(contract_addr: str, abi_path: str):
    addr = Web3.to_checksum_address(contract_addr)
    with open(abi_path, mode='r') as file:
        data = json.load(file)
        contract_abi = data['result']
    contract = w3.eth.contract(address=addr, abi=contract_abi)
    return contract


def sign_tx(tx_dict: dict, account: LocalAccount):
    signed_tx = account.sign_transaction(transaction_dict=tx_dict)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"oil harvest addr : {account.address} ==> tx_hash : {tx_hash.hex()}, status: {tx_receipt['status']}")


oilharv_contract = get_contract('0x60572F1631Bcf67afB60cD057D3c003Bc95B03C0', 'oil_dapp/harvest_abi.json')


def oil_harvest(key: str, toke_id=0):
    account: LocalAccount = Account.from_key(key)
    tx_dict = oilharv_contract.functions.claimRewards(toke_id).build_transaction(
        {
            'value': 0,
            'gas': 150000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account)


def oil_stake_nft(key: str, toke_id: int, amount=1):
    account: LocalAccount = Account.from_key(key)
    tx_dict = oilharv_contract.functions.stake(toke_id, amount).build_transaction(
        {
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
    sign_tx(tx_dict, account)
