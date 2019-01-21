import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

mypath = '/Users/SXZ/equity'

df = pd.read_excel(mypath + '/data1.xlsx', sheetname='Sheet1')

df = df.set_index('Date').dropna()


def datestr2num(s):
    return datetime.strptime(s, "%Y-%m-%d")

dfindex = pd.read_csv(mypath + '/^IXIC.csv', converters={0: datestr2num})[['Date', 'Adj Close']].set_index('Date')

#import pdb; pdb.set_trace()

df['NQ'] = dfindex['Adj Close']

dfratio = df / df.shift(1)

dfratio = dfratio.dropna()

nq = dfratio['NQ'].as_matrix().astype(np.float)

del dfratio['NQ']

stock = dfratio.as_matrix().astype(np.float)

reg = LinearRegression().fit(stock, nq)

res = reg.coef_ / sum(reg.coef_)

#import pdb; pdb.set_trace()

code_list = ['MSFT', 'AAPL', 'FB', 'INTC', 'CSCO',
             'CMCSA', 'PEP', 'NFLX', 'AMGN', 'ADBE',
             'PYPL', 'AVGO', 'TXN', 'COST', 'GILD',
             'NVDA', 'SBUX', 'WBA', 'CHTR', 'BIIB',
             'CHTR', 'MDLZ', 'ISRG']

ind_select = np.argwhere(res > 0.01)

code_select = []

for x in range(ind_select.shape[0]):
    code_select.append(code_list[x])

coef_sl = res[ind_select] / sum(res[ind_select])

coef_sl = np.round(coef_sl, 2)

stock_sl = df[code_select].as_matrix().astype(np.float)[560:]

repl_res = stock_sl.dot(coef_sl)

error = repl_res - df['NQ'].as_matrix().astype(np.float)

# return comparison
nqvalue = df['NQ'].as_matrix().astype(np.float)[560:]

nq_return = nqvalue / nqvalue[0]
repl_return = repl_res / repl_res[0]

plt.plot(repl_return)

plt.plot(nq_return, color='b')

ptf = dict(zip(code_select, coef_sl.flatten().tolist()))
print('portfolio is       ', ptf)

plt.show()

import pdb; pdb.set_trace()

#{'MSFT': 0.11, 'AAPL': 0.11, 'FB': 0.08, 'INTC': 0.04, 'CSCO': 0.08, 'CMCSA': 0.05, 'PEP': 0.02, 'NFLX': 0.07, 'AMGN': 0.06, 'ADBE': 0.03, 'PYPL': 0.04, 'AVGO': 0.04, 'TXN': 0.01, 'COST': 0.03, 'GILD': 0.03, 'NVDA': 0.04, 'SBUX': 0.01, 'WBA': 0.02, 'CHTR': 0.04, 'BIIB': 0.05, 'MDLZ': 0.04}
