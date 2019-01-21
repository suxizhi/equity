import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
from datetime import datetime
import pytz, tzlocal
from time import sleep, strftime, localtime
from ib_insync import *
import pandas as pd
import numpy as np


mypath = '/Users/SXZ/equity'

prop = {'MSFT': 0.11, 'AAPL': 0.11, 'FB': 0.08, 'INTC': 0.04, 'CSCO': 0.08, 'CMCSA': 0.05, 'PEP': 0.02, 'NFLX': 0.07, 'AMGN': 0.06, 'ADBE': 0.03, 'PYPL': 0.04, 'AVGO': 0.04, 'TXN': 0.01, 'COST': 0.03, 'GILD': 0.03, 'NVDA': 0.04, 'SBUX': 0.01, 'WBA': 0.02, 'CHTR': 0.04, 'BIIB': 0.05, 'MDLZ': 0.04}

arr_prop = np.array([np.float(x) for x in prop.values()])

symbols = list(prop.keys())

period = '1 W'
sym = symbols[0]

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=77)

symbols = list(set(symbols))

sym = symbols[0]

contract = Stock(sym, 'ARCA', 'USD')

bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='1 W', barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

df = util.df(bars)

dfPrice = pd.DataFrame(index=df.date)

for sym in symbols:
    
    print(sym)
    
    contract = Stock(sym, 'ARCA', 'USD')
    
    bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=period, barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)
    
    sleep(0.5)
    print('---------------')
    
    df = util.df(bars).set_index('date')
    
    dfPrice[sym] = df['close']

ib.disconnect()

price = dfPrice.iloc[-1]


shares = np.round(arr_prop / np.asarray(dfPrice.iloc[-1]) * 10 ** 5)

dict_shares = list(zip([x for x in prop.keys()], shares))

date_today = datetime.strftime(datetime.today(), '%Y%m%d')

writer = pd.ExcelWriter(mypath + '/betadata{}.xlsx'.format(date_today), engine='openpyxl')

dfPrice.to_excel(writer, sheet_name='Sheet1')
writer.save()
writer.close()

import pdb; pdb.set_trace()

# result
#[('MSFT', 42.0), ('AAPL', 111.0), ('FB', 178.0), ('INTC', 26.0), ('CSCO', 88.0), ('CMCSA', 72.0), ('PEP', 41.0), ('NFLX', 97.0), ('AMGN', 40.0), ('ADBE', 27.0), ('PYPL', 20.0), ('AVGO', 110.0), ('TXN', 4.0), ('COST', 14.0), ('GILD', 19.0), ('NVDA', 14.0), ('SBUX', 23.0), ('WBA', 6.0), ('CHTR', 37.0), ('BIIB', 15.0), ('MDLZ', 62.0)]


