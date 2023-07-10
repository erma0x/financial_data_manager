# Data manager

Scrape, download data and save into database each minute.

### Usage (with nohup)
   ```
./source/lunch_data_managers.sh
   ```

   ```
nohup python3 start_process.py SPY 1m >> logs/SPY_1m_output.log 2>> logs/SPY_1m_error.log &
   ```

   ```
nohup python3 ./source/data_manager_binance.py ETHUSDT 1m >> logs/ETHUSDT_1m_output.log 2>> ./logs/ETHUSDT_1m_error.log &
   ```

## Description

The code in this project performs the following tasks:

1. Downloads the last candlestick data for a specified financial asset using the `yfinance` library.
2. Saves the downloaded data into a SQLite database specified by the provided ticker and interval.

## Prerequisites

- Python 3.x
- Required libraries: `yfinance`, `sqlite3`

## Installation

1. Clone the repository or download the code files.
2. Install the required dependencies by running the following command:
   ```
   pip install yfinance
   ```

## Usage

   ```
   ./source/lunch_data_managers.sh
   ```


1. Run the script `source/data_manager.py` with the following command-line arguments:

   ```
   python3 script_name.py <ticker> <interval>
   ```

   - `<ticker>`: The ticker symbol of the financial asset (e.g., stock symbol).
   - `<interval>`: The time interval for data (e.g., "1d" for daily, "1h" for hourly, etc.).

2. The script will download the last candlestick data for the specified asset using the `yfinance` library.

3. The data will be saved into a SQLite database specified by the ticker and interval.

## Examples

```
python3 script_name.py AAPL 1d
```

## License

Mention the license under which the project is distributed.

## Contributors

Mention the contributors or provide guidelines for contributing to the project.

## Contact

Provide contact information or links for users to get in touch with the project maintainer or team.

This is a basic outline of the `README.md` file based on the code you provided. You can modify and expand it according to your project's specific requirements and additional details you want to provide.