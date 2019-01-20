import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
from datetime import datetime
import pytz, tzlocal
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import pandas as pd
import numpy as np
import statsmodels.api as sm


# Set up IB message handler to dump to pandas dataframe


def get_historical_data(sym):
    # define historical data handler for IB - this will populate our pandas data frame
    #    print(df)
    df = pd.DataFrame( columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'OpenInterest'])
    s = pd.Series()
    
    def my_error_handler(msg):
        print(msg)
    
    
    def historical_data_handler(msg):
        #        global df
        #    print (msg.reqId, msg.date, msg.open, msg.close, msg.high, msg.low)
        if ('finished' in str(msg.date)) == False:
            s = ([datetime.strptime(msg.date, '%Y%m%d'), msg.open, msg.high, msg.low, msg.close, msg.volume, 0])
#            print(s)
            df.loc[len(df)] = s
        
        else:
            df.set_index('Date',inplace=True)

    def makeStkContract(sym, exchange='SMART', currency='USD'): # Leave the exchange blank
        newContract = Contract()
        newContract.m_symbol = sym
        newContract.m_secType = 'STK'
        newContract.m_exchange = exchange
        newContract.m_currency = currency
        
        return newContract

    con = ibConnection(host='127.0.0.1',port=7497,clientId=77)
    con.registerAll(my_error_handler)
    con.unregister(my_error_handler, (message.historicalData, ))

    con.register(historical_data_handler, message.historicalData)
    con.connect()
    
    contract = makeStkContract(sym=sym, exchange='ARCA')
    
    con.reqHistoricalData(0, contract, '', '3 M', '1 day', 'TRADES', 1, 2)
    sleep(3)
    print('---------------')
    print(df.tail(2))
    con.disconnect()
    con.close()
    return df

def get_hedge_ratio(X, Y):
    '''Y = a * X + b + noise. return a'''
    X = sm.add_constant(X)
    #    print('X shape is       ', X.shape)
    #    print('Y shape is       ', Y.shape)
    model = sm.OLS(Y, X).fit()
    ratio = model.params[1]
    print('ratio is:      ', ratio)

#    if ratio >= 2.5:
#        return 'Hedging ratio too high.'
#    else:
    return ratio


def get_zscore(pair):
    
    lookback = 30
    zwindow = 20
    
    xsym = pair[0]
    ysym = pair[1]
    
    pairname = xsym + '-' + ysym
    
    for trade_date in list(dfPrice.index)[lookback+1:]:
        
        idx = dfPrice.index.get_loc(trade_date)
        data = dfPrice.iloc[idx - lookback : idx]
        
        X = data[xsym]
        Y = data[ysym]
        
        try:
            hedge_ratio = np.float(get_hedge_ratio(X, Y))
        
        except ValueError as e:
            #        log.debug(e)
            print('Exception')
            continue

        x_current_price = dfPrice.loc[trade_date, xsym]
        y_current_price = dfPrice.loc[trade_date, ysym]
        print(y_current_price, hedge_ratio, x_current_price)
        
        spread = y_current_price - hedge_ratio * x_current_price
        
        dfSpread.loc[trade_date, 'Spread'] = spread
        
        if len(dfSpread) <= 1:
            continue
        
        zscore = (spread - dfSpread.iloc[-zwindow:].Spread.mean()) / dfSpread.iloc[-zwindow:].Spread.std()

        dfZscore.loc[trade_date, pairname] = zscore



#symbols = ['AEP', 'DTE', 'XEL']
#pairs = [('AEP', 'DTE'), ('AEP', 'XEL')]

# List of stock symbols.
symbols = ['ETR', 'AEP', 'FHN', 'EXC', 'ATO', 'WM', 'DTE', 'WAL', 'AEE', 'FNB', 'WTFC', 'EWBC', 'HOMB', 'PNFP', 'NI', 'LPT', 'ROIC', 'HBAN', 'ONB', 'OGS', 'ECL', 'HWC', 'VLY', 'STL', 'RF', 'AWK', 'TCF', 'PNM', 'GBCI', 'BXS', 'ACC', 'WPC', 'WEC', 'DUK', 'ZION', 'MS', 'CNP', 'UMPQ', 'HON', 'FITB', 'RPAI', 'EQR', 'STI', 'CMA', 'ARE', 'ELS', 'FULT', 'AJG', 'UDR', 'UBSI', 'SUI', 'BRX', 'XEL', 'SR', 'RSG', 'NJR', 'PNW', 'NTRS', 'SNV', 'BOKF', 'PLD', 'IBKC', 'UMBF', 'MBFI', 'ATR', 'PNC', 'CFR', 'MMC']


pairs = [('AEP', 'DTE'), ('AEP', 'XEL'), ('ATO', 'EXC'), ('ATO', 'AEE'), ('DTE', 'XEL'), ('DUK', 'PNW'), ('ETR', 'WEC'), ('ETR', 'EXC'), ('ETR', 'AWK'), ('NI', 'XEL'), ('NI', 'CNP'), ('WEC', 'AEE'), ('WEC', 'AWK'), ('AJG', 'WM'), ('ECL', 'ATR'), ('ECL', 'RSG'), ('MMC', 'ATR'), ('MMC', 'WM'), ('MMC', 'HON'), ('BXS', 'WTFC'), ('BXS', 'WAL'), ('FNB', 'PNFP'), ('FNB', 'FHN'), ('FULT', 'GBCI'), ('FULT', 'HWC'), ('FULT', 'ONB'), ('FULT', 'TCF'), ('FULT', 'UBSI'), ('FULT', 'VLY'), ('FULT', 'UMBF'), ('FULT', 'WTFC'), ('FULT', 'UMPQ'), ('FULT', 'STL'), ('FULT', 'IBKC'), ('FULT', 'MBFI'), ('FULT', 'PNFP'), ('FULT', 'FHN'), ('FULT', 'WAL'), ('FULT', 'HOMB'), ('VLY', 'UMBF'), ('WTFC', 'UMPQ'), ('STL', 'PNFP'), ('PNFP', 'FHN'), ('BOKF', 'NTRS'), ('CFR', 'NTRS'), ('CMA', 'NTRS'), ('CMA', 'RF'), ('FITB', 'PNC'), ('FITB', 'MS'), ('HBAN', 'STI'), ('HBAN', 'RF'), ('NTRS', 'STI'), ('NTRS', 'ZION'), ('NTRS', 'RF'), ('PNC', 'MS'), ('SNV', 'EWBC'), ('STI', 'RF'), ('UDR', 'EQR'), ('ELS', 'SUI'), ('ELS', 'LPT'), ('LPT', 'WPC'), ('ARE', 'PLD'), ('ARE', 'ACC'), ('SR', 'PNM'), ('NJR', 'OGS'), ('ROIC', 'BRX'), ('RPAI', 'BRX')]


symbols = []
for pair in pairs:
    xsym = pair[0]
    ysym = pair[1]
    symbols.append(xsym)
    symbols.append(ysym)

symbols = list(set(symbols))

sym = symbols[0]
dfPrice = pd.DataFrame(index=get_historical_data(sym).index)

for sym in symbols:
    dfPrice[sym] = get_historical_data(sym)['Close']

print(dfPrice.head())

date_today = datetime.strftime(datetime.today(), '%Y%m%d')

mypath = '/Users/SXZ/equity'
writer = pd.ExcelWriter(mypath + '/stk{}.xlsx'.format(date_today), engine='openpyxl')
dfPrice.to_excel(writer, sheet_name='Sheet1')
writer.save()



dfPrice = pd.read_excel(mypath + '/stk{}.xlsx'.format(date_today))

dfSpread = pd.DataFrame(index=dfPrice.index)

dfZscore = pd.DataFrame(index=dfPrice.index)

for pair in pairs:
    get_zscore(pair)


writer = pd.ExcelWriter(mypath + '/zscore{}.xlsx'.format(date_today), engine='openpyxl')
dfZscore.to_excel(writer, sheet_name='Sheet1')
writer.save()

writer.close()

import pdb; pdb.set_trace()




