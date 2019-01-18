# coding = utf8
import pymysql
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import statsmodels.api as sm

from scipy import stats

mypath = '/Users/SXZ/equity'

user = 'root'
password = 'Canoe'
# specify database and cursor.
db = pymysql.connect(host='localhost', user=user, password=password, db='us_equity', charset='utf8mb4')
cursor = db.cursor()

pair = ['AON', 'MMC']
sql = 'select Date from AON'
df = pd.read_sql(sql, db).set_index('Date')

for sym in pair:
    sql = 'select Date, Adj_Close from '+ sym
    df[sym] = pd.read_sql(sql, db).set_index('Date')['Adj_Close']

cursor.close()

df = df.dropna()


total_amount = 5000

start_date = df.index[0]
end_date = df.index[-1]

lookback = 30
zwindow = 20

df_current_position = pd.DataFrame(index=df.index, columns=pair)
df_current_position = df_current_position.fillna(0)

df_target_position = pd.DataFrame(index=df.index, columns=pair)

df_target_position = pd.DataFrame(index=df.index, columns=pair)

df_spread = pd.DataFrame(columns=['Spread'])

# Calculate hedging ratio
def get_hedge_ratio(X, Y):
    '''Y = a * X + b + noise. return a'''
    X = sm.add_constant(X)
#    print('X shape is       ', X.shape)
#    print('Y shape is       ', Y.shape)
    model = sm.OLS(Y, X).fit()
    ratio = model.params[1]
    print('ratio is:      ', ratio)
    
    if ratio >= 2.5:
        return 'Hedging ratio too high.'
    else:
        return ratio


def get_previous_position(d):
    idx = df_current_position.index.get_loc(d)
#    import pdb; pdb.set_trace()
    xposition = df_current_position.iloc[idx-1][xsym]
    yposition = df_current_position.iloc[idx-1][ysym]
    return xposition, yposition


zscore_list = []

for trade_date in list(df.index)[lookback+1:]:
    
    xsym = pair[0]
    ysym = pair[1]
    idx = df.index.get_loc(trade_date)
    data = df.iloc[idx - lookback : idx]
  
    X = data[xsym]
    Y = data[ysym]
    
    try:
        hedge_ratio = get_hedge_ratio(X, Y)
    
    except ValueError as e:
#        log.debug(e)
        print('Exception')
        continue

    x_current_price = df.loc[trade_date, xsym]
    y_current_price = df.loc[trade_date, ysym]

    spread = y_current_price - hedge_ratio * x_current_price

    df_spread.loc[trade_date, 'Spread'] = spread
#    import pdb; pdb.set_trace()
    if len(df_spread) <= 1:
        continue

    zscore = (spread - df_spread.iloc[-zwindow:].Spread.mean()) / df_spread.iloc[-zwindow:].Spread.std()


    zscore_list.append(zscore)

    xposition, yposition = get_previous_position(trade_date)

    print('xposition, yposition:       ', xposition, yposition)

    if zscore > 0. and yposition > 0.:
        ytarget = 0.
        xtarget = 0.
     
        df_target_position.loc[trade_date, ysym] = ytarget
        df_target_position.loc[trade_date, xsym] = xtarget
        
        df_current_position.loc[trade_date, ysym] = ytarget
        df_current_position.loc[trade_date, xsym] = xtarget
        
#        import pdb; pdb.set_trace()
        continue

    if zscore < 0. and yposition < 0.:
        
        ytarget = 0.
        xtarget = 0.

        df_target_position.loc[trade_date, ysym] = ytarget
        
        print(df_target_position.loc[trade_date])
        
#        import pdb; pdb.set_trace()

        df_target_position.loc[trade_date, xsym] = xtarget
        
        df_current_position.loc[trade_date, ysym] = ytarget
        df_current_position.loc[trade_date, xsym] = xtarget
        
        continue


    if zscore < - 1. and yposition <= 0.:
        ytarget = total_amount / y_current_price
        xtarget = - hedge_ratio * ytarget

        df_target_position.loc[trade_date, ysym] = ytarget
        df_target_position.loc[trade_date, xsym] = xtarget
        
        df_current_position.loc[trade_date, ysym] = ytarget
        df_current_position.loc[trade_date, xsym] = xtarget
        
        continue

    if zscore > 1. and yposition >= 0.:
        ytarget = - total_amount / y_current_price
        xtarget = - hedge_ratio * ytarget

        df_target_position.loc[trade_date, ysym] = ytarget
        df_target_position.loc[trade_date, xsym] = xtarget

        df_current_position.loc[trade_date, ysym] = ytarget
        df_current_position.loc[trade_date, xsym] = xtarget
        
        continue


#print(df_target_position)


#writer = pd.ExcelWriter(mypath + '/target.xlsx', engine = 'openpyxl')
#df_target_position.to_excel(writer, 'Sheet1')
#writer.save()
#writer.close()

import pdb; pdb.set_trace()




def allocate():
    pass

def log():
    '''log actual holding position in current position.'''
#    df_current_position.loc[trade_date, xsym]
    pass








