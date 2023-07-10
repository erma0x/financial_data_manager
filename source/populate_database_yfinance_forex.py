import random as rnd
import yfinance as yf
import os

master_path = '/home/user/Documents/database/crypto/'

FOREX_CURRENCIES = ['EUR','CAD','AUD','CHF','JPY','NZD','GBP','MXN']
INTERVALS = ['5m','15m','30m','60m','90m','1d'] 

def switch(pair):
    return pair[3:]+pair[:3]

parameters = []

for i in FOREX_CURRENCIES:
    forex_currency_1 = i
    for j in FOREX_CURRENCIES:
        forex_currency_2 = j

        while forex_currency_2 == forex_currency_1:
            forex_currency_2 =rnd.choice(FOREX_CURRENCIES)

        for k in INTERVALS:
            parameters.append((forex_currency_1+forex_currency_2,k))

print(parameters)

for param in parameters:
    try:
        if not os.path.isdir(master_path + switch(param[0])):

            data = yf.download(tickers=param[0]+'=X', period='720d', interval=param[1])
            
            if data.empty:
                data = yf.download(tickers=param[0]+'=X', period='60d', interval=param[1])

            if not os.path.isdir(master_path+param[0]):
                os.makedirs(master_path+param[0])
            
            file_name = master_path+param[0]+'/'+param[0]+"_"+param[1]+'.csv'

            data.to_csv(file_name, sep='\t', encoding='utf-8')

    except KeyError as ke:
        print(ke)
