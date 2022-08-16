import sqlite3 as sq
from datetime import datetime
import time



def create_db():
    """Создание дб"""
    con = sq.connect('seeds.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS seeds(
        address TEXT,
        privatekey TEXT
    )""")
    con.commit()
    print('-----------------------------\nБаза данных создана')
    
def check(info):
    """Проверка есть ли адресс в дб"""
    con = sq.connect('seeds.db')
    cur = con.cursor()
    cur.execute(f"SELECT address FROM seeds WHERE address = ?", (info[0], ))
    data = cur.fetchone()
    if data is None:
        cur.execute("INSERT INTO seeds VALUES(?,?)", (info[0], info[1]))
        con.commit()
        return True
    else:
        con.commit()
        return False

def search_vivod(address):
    """Поиск адресса в дб из блока"""
    con = sq.connect('seeds.db')
    cur = con.cursor()
    cur.execute(f"SELECT address FROM seeds WHERE address = ?", [address])
    data = cur.fetchone()
    con.commit()
    if data is None:
        return False
    else:
        return True

def get_info_address(address):
    """Получение приват-кея"""
    con = sq.connect('seeds.db')
    cur = con.cursor()
    cur.execute("SELECT privatekey FROM seeds WHERE address = ?", [address])
    data = cur.fetchone()[0]
    con.commit()
    return data
    