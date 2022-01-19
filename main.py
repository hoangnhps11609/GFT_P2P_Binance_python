# This is a sample Python script.
from datetime import datetime

import requests as requests

from logging_helper import setup_logging
import sqlite3

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
logger = setup_logging()


# endpoint_p2p
def get_binance():
    try:
        endpoint = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
        data = {
            "page": 1,
            "rows": 20,
            "payTypes": [],
            "asset": "USDT",
            "tradeType": "BUY",
            "fiat": "VND",
            "publisherType": "merchant"
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(url=endpoint, json=data, headers=headers)
        content = response.json()['data']
        logger.info('Get response: success')
        avg(content)
    except:
        logger.error('Get response: error')


# Calcu aver

def avg(content):
    try:
        price = 0
        date = datetime.now()
        for each in content:
            price += float(each['adv']['price'])
        aver = price / len(content)
        logger.info('Avg: success')
        insert(date, price, aver)
    except:
        logger.error('Avg: error')


# Insert Data
def insert(date, price, aver):
    try:
        with sqlite3.connect('price.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "CREATE TABLE IF NOT EXISTS price (id Integer primary key autoincrement, Time datetime, Total float, Price float)")
            logger.info('CREATE TABLE: Success')
            curs.execute("INSERT INTO price(Time, Total, Price) VALUES (?,?,?)", (date, price, aver,))
            logger.info('INSERT: success')
            logger.info('------------------')
    except:
        logger.error('Insert: error')
        logger.info('------------------')


if __name__ == "__main__":
    get_binance()
