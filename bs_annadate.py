# 利用bs获取财报披露时间
import baostock as bs
import pandas as pd
import os
import time
import tushare as ts
import datetime as dt
from tqdm import tqdm


ts.set_token('640ab6afd74c33c9464b832ef12188365ead3168185f651bfeefa34f')
pro = ts.pro_api()

def get_annadate(code):
    time.sleep(0.1)
    try:
        df = pro.disclosure_date(ts_code=code).drop_duplicates(subset=['ts_code', 'end_date', 'pre_date'])
        if len(df) == 0:
            print(code + ' is empty')
            return code
        df.to_pickle(code+'.pkl')
        return None
    except:
        print(code + ' fail')
        return code

os.chdir(r'H:\data\annadate')
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
codeList = data.ts_code.to_list()

ansList = list(map(get_annadate,codeList))

res = list(filter(None, ansList))
while len(res)>0:
    ansList = list(map(get_annadate,res))
    res = list(filter(None, ansList))

##整理财务因子，使其成为标准结构
def reshape_financial(name,tem,datelist,name2):
    try:
        rev = pd.read_pickle(name)
        rev.index = [x.replace('-', '') for x in rev.index]
        combinedf = pd.concat([rev.stack(), tem.stack()], axis=1)
        combinedf.columns = [name[:-4], 'pre_date']
        combinedf['ts_code'] = [x[1] for x in combinedf.index]
        combinedf.dropna(subset=['pre_date'], inplace=True)
        combinedf.drop_duplicates(subset=['ts_code', 'pre_date'], keep='last', inplace=True)
        target = pd.pivot(combinedf, index='pre_date', columns='ts_code', values=name[:-4]).fillna(method='ffill')
        dates = [x.strftime('%Y%m%d') for x in list(pd.date_range(start=min(target.index), end=dt.datetime.today().strftime('%Y%m%d')))]
        tobeappend = pd.DataFrame(columns = target.columns,index = list(set(dates) - set(target.index)))
        finaltarget = pd.concat([target, tobeappend]).sort_index().fillna(method='ffill').dropna(how = 'all').loc[datelist,:]
        finaltarget.to_pickle('../' + name2 + '/' + name)
        return
    except:
        print(name+' fail')
        return

def reshape_path(path,name2):
    datedf = pro.query('trade_cal', start_date=20110101, end_date=dt.datetime.today().strftime('%Y%m%d'))
    datelist = datedf[datedf.is_open == 1].copy()
    datelist = datelist.cal_date.to_list()
    os.chdir(r'H:\data\annadate')

    Lis = os.listdir()
    Li = list(map(pd.read_pickle, Lis))
    df = pd.concat(Li)
    df0 = df.sort_values(['ts_code', 'end_date', 'pre_date']).drop_duplicates(subset=['ts_code', 'end_date'],keep='first')
    tem = pd.pivot(df0, index='end_date', columns='ts_code', values='pre_date').dropna(how='all')
    tem.columns = [x[:6] for x in tem.columns]
    os.chdir(path)
    Lis = os.listdir()
    for i in tqdm(Lis):
        reshape_financial(i, tem,datelist,name2)

reshape_path('H:\data\lrb_factor','lrb_factor2')
path = 'H:\data\lrb_factor'
name2 = 'lrb_factor2'
reshape_path(r'H:\data\xjllb_factor','xjllb_factor2')
reshape_path(r'H:\data\zcfzb_factor','zcfzb_factor2')
