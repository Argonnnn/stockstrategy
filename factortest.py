import pandas as pd
import numpy as np
import tushare as ts
import datetime as dt
import os
from time import time
import matplotlib.pyplot as plt

path = r'D:\factor\basic'
# path = r'H:\data\factor\basic'
os.chdir(path)
pctchg = pd.read_pickle('pct_chg.pkl').sort_index().fillna(0)
close = pd.read_pickle('close.pkl').sort_index()
adj = pd.read_pickle('adj_factor.pkl')
adj = adj.sort_index().reset_index().drop_duplicates(subset = 'index',keep = 'first').set_index(keys = 'index',drop = True)
adj = adj.loc[:,close.columns]
adjclo = close*adj
n = 5
mom5 = adjclo/adjclo.shift(n) - 1

startDay = '20110104'
endDay = '20211223'
factor = mom5
def ncut(series,n):
    if n==0:
        print('n = 1，fail')
        return
    try:
        label = list(range(n))
        cut = pd.qcut(series,n,labels = label)
        return cut
    except:
        print(str(n)+' fail,try '+str(n-1))
        return(ncut(series,n-1))
factor1 = factor.apply(ncut,args=(10,),axis = 1)

s = (factor1 == 9)*1
a = s.sum(axis = 1)
sa = s.divide(a,axis = 0)
sa.dropna(how = 'all',inplace = True)
accu = (pctchg.loc[:,sa.columns] *sa.shift(2)).sum(axis=1)

netvalue = (1 + accu/100).cumprod()
netvalue.plot()
def describe_portfolio(cangwei,pct = pctchg,rf = 0.022):
    portfolioChg = (pct.loc[cangwei.index,cangwei.columns]*cangwei.shift(2)).sum(axis = 1)
    netvalue = (1+portfolioChg/100).cumprod()
    desDict = {}
    desDict['gain2loss'] = -(portfolioChg[portfolioChg>0]).mean()/(portfolioChg[portfolioChg<0]).mean()
    desDict['winrate'] = len(portfolioChg[portfolioChg>0])/len(portfolioChg)
    desDict['withdraw250'] = np.nanmax(1 - netvalue / netvalue.rolling(250).max())
    desDict['sharperatio'] =((netvalue[-1])**(250/len(netvalue))-1-rf)/np.nanstd(portfolioChg/100)/np.sqrt(250)
    return portfolioChg,netvalue,desDict

def get_ICs(factor,pct = pctchg,n = 2,method ='default'):
    if method == 'rank_IC':
        factor = factor.rank(axis = 1)
        pctchg = pct.rank(axis = 1)
    factest = factor.dropna(how='all').shift(n).dropna(how='all')
    pchg = pct.loc[factest.index, factest.columns]
    facmean = factest.T.sub(factest.mean(axis=1)).T
    pctmean = pchg.T.sub(pchg.mean(axis=1)).T
    pctmean = pctmean[facmean.notnull()]
    cov = np.diag(facmean.fillna(0).dot(pctmean.fillna(0).T))
    moment = (((facmean ** 2).sum(axis=1)) ** 0.5) * (((pctmean ** 2).sum(axis=1)) ** 0.5)
    return cov/moment


def describe_factor(fac,pct = pctchg,n= 10,rf = 0.022):
    facBin = fac.apply(ncut,args=(n,),axis = 1)
    positions = [(facBin==x)*1 for x in range(n)]
    positions = [p.divide(p.sum(axis = 1),axis = 0) for p in positions]
    return positions

pos = describe_factor(mom5)
a,b,c = [describe_portfolio(x.dropna(how = 'all')) for x in pos]

