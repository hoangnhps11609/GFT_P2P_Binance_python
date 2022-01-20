# This is a sample Python script.
from datetime import datetime

import requests as requests

from logging_helper import setup_logging
import sqlite3

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
logger = setup_logging()

# main
def run():
    content = get_binance()
    if content:
        price = calcu_avg(content)
        insert(price)

# get binance
def get_binance():
    # get response
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
        if response.ok:
            content = response.json()
            return content
        else:
            logger.info('API not response')
            return None
    except:
        logger.error('Get response: error')


# calcu avg
def calcu_avg(content):
    price = 0
    for each in content['data']:
        price += float(each['adv']['price'])
    price /= len(content)
    return price


# insert data
def insert(price):
        with sqlite3.connect('price.db') as conn:
            curs = conn.cursor()
            date = datetime.now()
            curs.execute(
                "CREATE TABLE IF NOT EXISTS price (id Integer primary key autoincrement, DateTime date, Price float)")
            logger.info('CREATE TABLE: Success')
            curs.execute("INSERT INTO price(DateTime, Price) VALUES (?,?)", (date, price,))
            logger.info('INSERT: success')


if __name__ == "__main__":
    logger.info('--------------------------------')
    logger.info('APP START')
    run()
    logger.info("APP END")
