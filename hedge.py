import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from datetime import datetime
import pytz, tzlocal
from time import sleep, strftime, localtime

import pandas as pd
import numpy as np
import statsmodels.api as sm



date_today = datetime.strftime(datetime.today(), '%Y%m%d')

mypath = '/Users/SXZ/equity'

def get_hedge_ratio(X, Y):
    '''Y = a * X + b + noise. return a'''
#    X = sm.add_constant(X)
    #    print('X shape is       ', X.shape)
    #    print('Y shape is       ', Y.shape)
    model = sm.OLS(Y, X).fit()
    ratio = model.params[0]
    print('ratio is:      ', ratio)

    return ratio

def get_zscore_nd_ratio(pair):
    
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
        
        dfHedgeRatio.loc[trade_date, pairname] = hedge_ratio
    
        dfZscore.loc[trade_date, pairname] = zscore



pairs = [('AEP', 'DTE'), ('AEP', 'XEL'), ('ATO', 'EXC'), ('ATO', 'AEE'), ('DTE', 'XEL'), ('DUK', 'PNW'), ('ETR', 'WEC'), ('ETR', 'EXC'), ('ETR', 'AWK'), ('NI', 'XEL'), ('NI', 'CNP'), ('WEC', 'AEE'), ('WEC', 'AWK'), ('AJG', 'WM'), ('ECL', 'ATR'), ('ECL', 'RSG'), ('MMC', 'ATR'), ('MMC', 'WM'), ('MMC', 'HON'), ('BXS', 'WTFC'), ('BXS', 'WAL'), ('FNB', 'PNFP'), ('FNB', 'FHN'), ('FULT', 'GBCI'), ('FULT', 'HWC'), ('FULT', 'ONB'), ('FULT', 'TCF'), ('FULT', 'UBSI'), ('FULT', 'VLY'), ('FULT', 'UMBF'), ('FULT', 'WTFC'), ('FULT', 'UMPQ'), ('FULT', 'STL'), ('FULT', 'IBKC'), ('FULT', 'MBFI'), ('FULT', 'PNFP'), ('FULT', 'FHN'), ('FULT', 'WAL'), ('FULT', 'HOMB'), ('VLY', 'UMBF'), ('WTFC', 'UMPQ'), ('STL', 'PNFP'), ('PNFP', 'FHN'), ('BOKF', 'NTRS'), ('CFR', 'NTRS'), ('CMA', 'NTRS'), ('CMA', 'RF'), ('FITB', 'PNC'), ('FITB', 'MS'), ('HBAN', 'STI'), ('HBAN', 'RF'), ('NTRS', 'STI'), ('NTRS', 'ZION'), ('NTRS', 'RF'), ('PNC', 'MS'), ('SNV', 'EWBC'), ('STI', 'RF'), ('SR', 'PNM'), ('NJR', 'OGS'), ('ROIC', 'BRX'), ('RPAI', 'BRX')]

#('UDR', 'EQR'), ('ELS', 'SUI'), ('ELS', 'LPT'), ('LPT', 'WPC'), ('ARE', 'PLD'), ('ARE', 'ACC')

symbols = []
for pair in pairs:
    xsym = pair[0]
    ysym = pair[1]
    symbols.append(xsym)
    symbols.append(ysym)


dfPrice = pd.read_excel(mypath + '/stk{}.xlsx'.format(date_today)).set_index('date')

dfSpread = pd.DataFrame(index=dfPrice.index)

dfZscore = pd.DataFrame(index=dfPrice.index)

dfHedgeRatio = pd.DataFrame(index=dfPrice.index)

for pair in pairs:
    
    get_zscore_nd_ratio(pair)



writer = pd.ExcelWriter(mypath + '/hedge{}.xlsx'.format(date_today), engine='openpyxl')

dfZscore.to_excel(writer, sheet_name='Sheet1')

dfHedgeRatio.to_excel(writer, sheet_name='Sheet2')

writer.save()

writer.close()

import pdb; pdb.set_trace()
