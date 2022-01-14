import pandas as pd
import numpy as np
import datetime as dt
import tushare as ts
import os
import time
import matplotlib.pyplot as plt
ts.set_token('640ab6afd74c33c9464b832ef12188365ead3168185f651bfeefa34f')
pro = ts.pro_api()

#测试
code = '600000.SH'
startDay = '20200101'
endDay = '20211207'
n = 20

price = ts.pro_bar(ts_code=code, asset='E',  adj='qfq',start_date=startDay, end_date=endDay).set_index('trade_date')
df = pro.query('daily_basic', ts_code=code, start_date=startDay,end_date = endDay,
               fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb').set_index('trade_date')

tar = pd.concat([price,df.loc[:,['pe','volume_ratio','turnover_rate']]],axis = 1 ).sort_index(ascending= True)
tar['rollingvar'] = tar.pct_chg.rolling(window=n).var()
tar = tar.dropna()
fig = plt.figure(111)
ax1 = fig.add_subplot(222)
tar.loc[:,['rollingvar','pe','close']].plot()
ax = ax1.twinx()
tar.close.plot()
