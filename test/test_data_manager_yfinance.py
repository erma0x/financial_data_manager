import sqlite3
import pytest
from datetime import datetime
import pandas as pd

from ..source.data_manager_yfinance import download_last_candle, save_to_database

@pytest.fixture
def db_file():
    db_file = 'test.db'
    yield db_file
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS candles;")
    conn.commit()
    conn.close()

def test_download_last_candle():
    # Add test cases for download_last_candle function
    pass

def test_save_to_database(db_file):
    last_candle = pd.Series({'Open': 100.0, 'High': 110.0, 'Low': 90.0, 'Close': 105.0, 'Volume': 1000}, name=datetime.now())
    save_to_database(last_candle, db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='candles';")
    assert cursor.fetchone() is not None

    # Check if the data was inserted correctly
    cursor.execute("SELECT * FROM candles")
    result = cursor.fetchone()
    assert result[0] == last_candle.name.to_pydatetime().strftime("%Y-%m-%d %H:%M:%S")
    assert result[1] == last_candle['Open']
    assert result[2] == last_candle['High']
    assert result[3] == last_candle['Low']
    assert result[4] == last_candle['Close']
    assert result[5] == last_candle['Volume']

    conn.close()

def test_main(mocker):
    # Mock the market_is_open function to return True
    mocker.patch('my_script.market_is_open', return_value=True)

    # Add test cases for the main function
    pass
