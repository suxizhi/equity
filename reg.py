import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

import matplotlib.pyplot as plt

mypath = '/Users/SXZ/equity'

df = pd.read_excel(mypath + '/data1.xlsx', sheetname='Sheet2')

df = df.set_index('Date').dropna()

dfratio = df / df.shift(1)

dfratio = dfratio.dropna()

arr = dfratio.as_matrix().astype(np.float)

nq = arr[:, 0]
stock = arr[:, 1:]


reg = LinearRegression().fit(stock, nq)

res = reg.coef_ / sum(reg.coef_)

code_list = ['MSFT', 'AAPL', 'FB', 'INTC', 'CSCO',
             'CMCSA', 'PEP', 'NFLX', 'AMGN', 'ADBE',
             'PYPL', 'AVGO', 'TXN', 'COST', 'GILD',
             'NVDA', 'SBUX', 'BKNG', 'WBA', 'CHTR', 'BIIB']

ind_select = np.argwhere(res > 0.01)

code_select = []

for x in range(ind_select.shape[0]):
    code_select.append(code_list[x])

coef_sl = res[ind_select] / sum(res[ind_select])

coef_sl = np.round(coef_sl, 2)

stock_sl = df[code_select].as_matrix().astype(np.float)
rep_res = stock_sl.dot(coef_sl)

error = rep_res - df['Adj Close'].as_matrix().astype(np.float)

# return comparison
nqvalue = df['Adj Close'].as_matrix().astype(np.float)
nq_return = nqvalue / nqvalue[0]
rep_return = rep_res / rep_res[0]

plt.plot(rep_return)

plt.plot(nq_return, color='b')

ptf = dict(zip(code_select, coef_sl.flatten().tolist()))
print('portfolio is       ', ptf)

plt.show()

import pdb; pdb.set_trace()

# 'MSFT' 0.05, 'AAPL' 0.06, 'FB' 0.06, 'CSCO' 0.12,
#'CMCSA' 0.05, 'PEP' 0.17, 'AMGN' 0.08, 'ADBE' 0.03
#'PYPL' 0.04, 'TXN' 0.14, 'COST' 0.15, 'GILD' 0.05,
#'SBUX' 0.07, 'CHTR' 0.05]

#array([ 0.05240678,  0.05755938,  0.06383678, -0.0061136 ,  0.12471774,
#    0.04776778,  0.17234142, -0.00565503,  0.07673657,  0.02567368,
#    0.04214532, -0.08221469,  0.14172636,  0.15430429,  0.04970746,
#    -0.00818287,  0.07249325, -0.03178175,  0.00871812,  0.05107799,
#    -0.00726496])
