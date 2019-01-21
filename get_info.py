import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from datetime import datetime
import pytz, tzlocal
from time import sleep, strftime, localtime

import pandas as pd
import numpy as np

from ib_insync import *

date_today = datetime.strftime(datetime.today(), '%Y%m%d')

mypath = '/Users/SXZ/equity'

df = pd.read_excel(mypath + '/hedge{}.xlsx'.format(date_today), sheetname= 'Sheet4')

symbols = list(df['symbol'])

params = ['longName', 'category', 'subcategory']
df2 = pd.DataFrame(columns=params)

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=77)

for sym in symbols:
    
    contract = Stock(sym, 'ARCA', 'USD')
    
    cds = ib.reqContractDetails(contract)
    print(ContractDetails.defaults)
#    import pdb; pdb.set_trace()
    ss = pd.Series({key: getattr(cds[0], key) for key in params})
    
    ss['symbol'] = sym
    df2.loc[len(df2)] = ss
    sleep(0.1)


ib.disconnect()

writer = pd.ExcelWriter(mypath + '/hedge{}.xlsx'.format(date_today), engine='openpyxl')

df2.to_excel(writer, sheet_name='Sheet5')

writer.save()

writer.close()

print(df2.head(2))

import pdb; pdb.set_trace()
