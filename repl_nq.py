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
from hist_data import get_historical_data

mypath = '/Users/SXZ/equity'

prop = {'MSFT': 0.11, 'AAPL': 0.11, 'FB': 0.08, 'INTC': 0.04, 'CSCO': 0.07, 'CMCSA': 0.06, 'PEP': 0.02, 'NFLX': 0.09, 'AMGN': 0.06, 'ADBE': 0.03, 'PYPL': 0.04, 'AVGO': 0.04, 'TXN': 0.01, 'COST': 0.04, 'GILD': 0.03, 'NVDA': 0.04, 'SBUX': 0.06, 'BKNG': 0.02, 'WBA': 0.02, 'CHTR': 0.03}

arr_prop = np.array([np.float(x) for x in prop.values()])

symbols = list(prop.keys())

period = '1 W'
sym = symbols[0]
dfPrice = pd.DataFrame(index=get_historical_data(sym, period=period).index)


for sym in symbols:
    dfPrice[sym] = get_historical_data(sym, period=period)['Close']

price = dfPrice.iloc[-1]


shares = np.round(arr_prop / np.asarray(dfPrice.iloc[-1]) * 10 ** 5)

dict_shares = list(zip([x for x in prop.keys()], shares))

date_today = datetime.strftime(datetime.today(), '%Y%m%d')

writer = pd.ExcelWriter(mypath + '/betadata{}.xlsx'.format(date_today), engine='openpyxl')

dfPrice.to_excel(writer, sheet_name='Sheet1')
writer.save()
writer.close()

import pdb; pdb.set_trace()

# [('MSFT', 102.0), ('AAPL', 70.0), ('FB', 53.0), ('INTC', 81.0), ('CSCO', 155.0), ('CMCSA', 166.0), ('PEP', 18.0), ('NFLX', 27.0), ('AMGN', 29.0), ('ADBE', 12.0), ('PYPL', 44.0), ('AVGO', 15.0), ('TXN', 10.0), ('COST', 19.0), ('GILD', 43.0), ('NVDA', 25.0), ('SBUX', 93.0), ('BKNG', 1.0), ('WBA', 28.0), ('CHTR', 10.0)]




