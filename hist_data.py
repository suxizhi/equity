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


def get_historical_data(sym, period='3 M'):
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
    
    con = ibConnection(host='127.0.0.1',port=4002,clientId=77)
    con.registerAll(my_error_handler)
    con.unregister(my_error_handler, (message.historicalData, ))

    con.register(historical_data_handler, message.historicalData)
    con.connect()

    contract = makeStkContract(sym=sym, exchange='ARCA')
    
    con.reqHistoricalData(0, contract, '', period, '1 day', 'TRADES', 1, 2)
    sleep(3)
    print('---------------')
    print(df.tail(2))
    con.disconnect()
    con.close()
    return df
