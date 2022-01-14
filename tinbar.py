import pandas as pd
import numpy as np
import datetime as dt
import tushare as ts
import os
pro = ts.pro_api()

path = r'D:\factor'
# path = r'H:\data\factor'
os.chdir(path + r'\basic')
open = pd.read_pickle('open.pkl')
close = pd.read_pickle('close.pkl')
high = pd.read_pickle('high.pkl')
low = pd.read_pickle('low.pkl')

bar = abs(open-close)
uptin = (high*2-open-close-bar)/2
downtin = (open+close-2*low-bar)/2

down2bar = downtin/bar
down2bar[down2bar<1] = np.nan

