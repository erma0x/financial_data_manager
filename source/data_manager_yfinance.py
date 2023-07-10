import yfinance as yf
import sys
import sqlite3

from market_open import market_is_open

def download_last_candle(ticker, interval):
    data = yf.download(tickers=ticker,interval=interval)
    if len(data) > 0:
        last_candle = data.iloc[-1]
        return last_candle
    return None

def save_to_database(last_candle, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS candles
                      (timestamp TEXT, open FLOAT, high FLOAT,
                       low FLOAT, close FLOAT, volume INTEGER)''')

    # Insert the data into the table
    cursor.execute('''INSERT INTO candles VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (last_candle.name.to_pydatetime().strftime("%Y-%m-%d %H:%M:%S"), last_candle['Open'], last_candle['High'],
                    last_candle['Low'].astype(float), last_candle['Close'].astype(float), last_candle['Volume']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <ticker> <interval>")
        print("Example: python3 data_manager.py SPY 1m")

        sys.exit(1)

    ticker = sys.argv[1]
    interval = sys.argv[2]
    db_file = f'database/{ticker}_{interval}.db'  # Path to the SQLite database file

    if market_is_open():
        # Download the last candle for the specified asset
        last_candle = download_last_candle(ticker, interval)

        # Save the data to the database
        if last_candle is not None:
            save_to_database(last_candle, db_file)
