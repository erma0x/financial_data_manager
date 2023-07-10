import yfinance as yf
import datetime
import os

master_path = '/home/user/Documents/database/crypto/'

CRYPTO_CURRENCIES = ['BTC','ETH','XRP','AAVE','ADA','TRX','LTC','DOT','MATIC','SHIB']
INTERVALS = ['5m','15m','30m','60m','90m','1d'] 

parameters = []

for i in CRYPTO_CURRENCIES:
    for k in INTERVALS:
        parameters.append((i+'-USD',k))

print(parameters)

now = datetime.datetime.now()
delta = datetime.timedelta(days=720)
start_720d = now - delta

delta = datetime.timedelta(days=60)
start_60d = now - delta

for param in parameters:
    try:
        data = yf.download(tickers=param[0]+'', start=start_720d ,end=now, interval=param[1])
        
        if data.empty:
            data = yf.download(tickers=param[0], start=start_60d ,end=now, interval=param[1])

        if not os.path.isdir(master_path+param[0].replace('-','')):
            os.makedirs(master_path+param[0].replace('-',''))
        
        file_name = master_path+param[0].replace('-','')+'/'+param[0].replace('-','')+"_"+param[1]+'.csv'

        data.to_csv(file_name, sep='\t', encoding='utf-8')

    except KeyError as ke:
        print(ke)
        
