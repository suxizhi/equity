import pandas as pd
import numpy as np
import pymysql
from datetime import date

mypath = '/Users/SXZ/equity'

user = 'root'
password = 'Canoe'

# specify database and cursor.
db = pymysql.connect(host='localhost', user=user, password=password, db='us_equity', charset='utf8mb4')
cursor = db.cursor()

code_list = ['MSFT', 'AAPL', 'FB', 'INTC', 'CSCO',
             'CMCSA', 'PEP', 'NFLX', 'AMGN', 'ADBE',
             'PYPL', 'AVGO', 'TXN', 'COST', 'GILD',
             'NVDA', 'SBUX', 'WBA', 'CHTR', 'BIIB',
             'MDLZ', 'ISRG', 'CELG']


sql = "select * from MSFT"
index = pd.read_sql(sql, db)['Date']

df = pd.DataFrame(index=index, columns=code_list)

#code_list = ['FB', 'PYPL']
for code in code_list:
    sql = "select * from " + code
    
    df[code] = pd.read_sql(sql, db).set_index('Date')['Adj_Close']


writer = pd.ExcelWriter(mypath + '/data1.xlsx', engine = 'openpyxl')

df.to_excel(writer, 'Sheet1')
writer.save()
writer.close()

db.close()

import pdb; pdb.set_trace()

