import pytest
import asyncio
import os
from datetime import datetime

from binance import AsyncClient, BinanceSocketManager

import sqlite3

from ..source.data_manager_binance import download_last_candle, save_to_database

@pytest.fixture
async def client():
    client = await AsyncClient.create()
    yield client
    await client.close_connection()

@pytest.fixture
async def token_pair():
    return 'BNBUSDT'  # Replace with your desired token pair

@pytest.fixture
def db_file():
    db_file = 'test.db'
    yield db_file
    os.remove(db_file)  # Remove the test database file after the tests

@pytest.fixture
async def candle(client, token_pair):
    return await download_last_candle(client, token_pair=token_pair)

def test_timestamp_to_date():
    # Add test cases for timestamp_to_date function
    pass

def test_save_to_database(candle, db_file):
    save_to_database(last_candle=candle, db_file=db_file)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='candles';")
    assert cursor.fetchone() is not None

    # Check if the data was inserted correctly
    cursor.execute("SELECT * FROM candles")
    result = cursor.fetchone()
    assert result[0] == datetime.fromtimestamp(int(candle[0][:-3])).strftime('%d-%m-%Y %H:%M:%S')
    assert result[1] == float(candle[1])
    assert result[2] == float(candle[2])
    assert result[3] == float(candle[3])
    assert result[4] == float(candle[4])
    assert result[5] == float(candle[5])

    conn.close()

@pytest.mark.asyncio
async def test_download_last_candle(client, token_pair):
    candle = await download_last_candle(client, token_pair=token_pair)
    # Add assertions to check if the candle data is correct
    assert isinstance(candle, tuple)
    assert len(candle) == 6

@pytest.mark.asyncio
async def test_main():
    # Add test cases for the main function
    pass
