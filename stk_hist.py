import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
from datetime import datetime
import pytz, tzlocal
from time import sleep, strftime, localtime
#from ib.ext.Contract import Contract
#from ib.opt import ibConnection, message
from ib_insync import *

import pandas as pd
import numpy as np
import statsmodels.api as sm
#from hist_data import get_historical_data


date_today = datetime.strftime(datetime.today(), '%Y%m%d')

mypath = '/Users/SXZ/equity'

# Set up IB message handler to dump to pandas dataframe



#symbols = ['AEP', 'DTE', 'XEL']
#pairs = [('AEP', 'DTE'), ('AEP', 'XEL')]

# List of stock symbols.
#symbols = ['ETR', 'AEP', 'FHN', 'EXC', 'ATO', 'WM', 'DTE', 'WAL', 'AEE', 'FNB', 'WTFC', 'EWBC', 'HOMB', 'PNFP', 'NI', 'LPT', 'ROIC', 'HBAN', 'ONB', 'OGS', 'ECL', 'HWC', 'VLY', 'STL', 'RF', 'AWK', 'TCF', 'PNM', 'GBCI', 'BXS', 'ACC', 'WPC', 'WEC', 'DUK', 'ZION', 'MS', 'CNP', 'UMPQ', 'HON', 'FITB', 'RPAI', 'EQR', 'STI', 'CMA', 'ARE', 'ELS', 'FULT', 'AJG', 'UDR', 'UBSI', 'SUI', 'BRX', 'XEL', 'SR', 'RSG', 'NJR', 'PNW', 'NTRS', 'SNV', 'BOKF', 'PLD', 'IBKC', 'UMBF', 'MBFI', 'ATR', 'PNC', 'CFR', 'MMC']


pairs = [('AEP', 'DTE'), ('AEP', 'XEL'), ('ATO', 'EXC'), ('ATO', 'AEE'), ('DTE', 'XEL'), ('DUK', 'PNW'), ('ETR', 'WEC'), ('ETR', 'EXC'), ('ETR', 'AWK'), ('NI', 'XEL'), ('NI', 'CNP'), ('WEC', 'AEE'), ('WEC', 'AWK'), ('AJG', 'WM'), ('ECL', 'ATR'), ('ECL', 'RSG'), ('MMC', 'ATR'), ('MMC', 'WM'), ('MMC', 'HON'), ('BXS', 'WTFC'), ('BXS', 'WAL'), ('FNB', 'PNFP'), ('FNB', 'FHN'), ('FULT', 'GBCI'), ('FULT', 'HWC'), ('FULT', 'ONB'), ('FULT', 'TCF'), ('FULT', 'UBSI'), ('FULT', 'VLY'), ('FULT', 'UMBF'), ('FULT', 'WTFC'), ('FULT', 'UMPQ'), ('FULT', 'STL'), ('FULT', 'IBKC'), ('FULT', 'MBFI'), ('FULT', 'PNFP'), ('FULT', 'FHN'), ('FULT', 'WAL'), ('FULT', 'HOMB'), ('VLY', 'UMBF'), ('WTFC', 'UMPQ'), ('STL', 'PNFP'), ('PNFP', 'FHN'), ('BOKF', 'NTRS'), ('CFR', 'NTRS'), ('CMA', 'NTRS'), ('CMA', 'RF'), ('FITB', 'PNC'), ('FITB', 'MS'), ('HBAN', 'STI'), ('HBAN', 'RF'), ('NTRS', 'STI'), ('NTRS', 'ZION'), ('NTRS', 'RF'), ('PNC', 'MS'), ('SNV', 'EWBC'), ('STI', 'RF'), ('SR', 'PNM'), ('NJR', 'OGS'), ('ROIC', 'BRX'), ('RPAI', 'BRX')]

#('UDR', 'EQR'), ('ELS', 'SUI'), ('ELS', 'LPT'), ('LPT', 'WPC'), ('ARE', 'PLD'), ('ARE', 'ACC'),

symbols = []
for pair in pairs:
    xsym = pair[0]
    ysym = pair[1]
    symbols.append(xsym)
    symbols.append(ysym)



ib = IB()
ib.connect('127.0.0.1', 4002, clientId=77)

symbols = list(set(symbols))

sym = symbols[0]

contract = Stock(sym, 'SMART', 'USD')

duration = '6 M'
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration, barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

df = util.df(bars)

dfPrice = pd.DataFrame(index=df.date)

for sym in symbols:

    print(sym)

    contract = Stock(sym, 'SMART', 'USD')

    bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration, barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

    sleep(0.1)
    print('---------------')

    df = util.df(bars).set_index('date')

    dfPrice[sym] = df['close']

ib.disconnect()

print(dfPrice.head())


writer = pd.ExcelWriter(mypath + '/stk{}.xlsx'.format(date_today), engine='openpyxl')
dfPrice.to_excel(writer, sheet_name='Sheet1')
writer.save()

writer.close()


import pdb; pdb.set_trace()




