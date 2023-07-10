#!/usr/bin/env python3
# coding: utf-8
import asyncio
from datetime import datetime

from binance import AsyncClient, BinanceSocketManager

import sqlite3

def timestamp_to_date(time):
    time=str(time)
    return(datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))

async def download_last_candle(client,token_pair='BNBUSDT'):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=token_pair) as stream:        
        res = await stream.recv()
        #print('date: ',timestamp_to_date(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])
        last_candle = timestamp_to_date(res['k']['T']),res['k']['o'], res['k']['h'], res['k']['l'], res['k']['c'], res['k']['V']
        return(last_candle) # closing price

def save_to_database(last_candle, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS candles
                      (timestamp TEXT, open FLOAT, high FLOAT,
                       low FLOAT, close FLOAT, volume FLOAT)''')

    # Insert the data into the table
    cursor.execute('''INSERT INTO candles VALUES (?, ?, ?, ?, ?, ?)''',
                   (last_candle[0], float(last_candle[1]), float(last_candle[2]),
                    float(last_candle[3]), float(last_candle[4]), float(last_candle[5])))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

import time, sys

async def main():

    if len(sys.argv) != 3:
        print("Usage: python3 script.py <ticker> <interval>")
        print("Example: python3 data_manager.py SPY 1m")

        sys.exit(1)

    TICKER = sys.argv[1]
    INTERVAL = sys.argv[2]

    client = await AsyncClient.create()

    db_file = f'database/{TICKER}_{INTERVAL}.db'  # Path to the SQLite database file

    while True:
        
        last_candle = await download_last_candle( client, token_pair = TICKER)
        print(last_candle)
        save_to_database(db_file=db_file, last_candle=last_candle)
        time.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())