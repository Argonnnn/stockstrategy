import pandas as pd
import numpy as np
import datetime as dt
import tushare as ts
import os
import time
ts.set_token('640ab6afd74c33c9464b832ef12188365ead3168185f651bfeefa34f')
pro = ts.pro_api()

def get_lrb(code):
    time.sleep(0.1)
    try:
        url = 'https://quotes.money.163.com/service/lrb_%s.html'
        url = url%(code)
        df = pd.read_csv(url,encoding='gb2312')
        df.to_pickle(r'H:\data\lrb\\'+code+'.pkl')
        return 1
    except:
        print(code+' fail')
        return code
def get_zcfzb(code):
    time.sleep(0.1)
    try:
        url = 'https://quotes.money.163.com/service/zcfzb_%s.html'
        url = url%(code)
        df = pd.read_csv(url,encoding='gb2312')
        df.to_pickle(r'H:\data\zcfzb\\'+code+'.pkl')
        return 1
    except:
        print(code+' fail')
        return code
def get_xjllb(code):
    time.sleep(0.1)
    try:
        url = 'https://quotes.money.163.com/service/xjllb_%s.html'
        url = url%(code)
        df = pd.read_csv(url,encoding='gb2312')
        df.to_pickle(r'H:\data\xjllb\\'+code+'.pkl')
        return 1
    except:
        print(code+' fail')
        return code

##从163获取全部的财务报表并整合为财务因子数据，获取过程暂时未改进
class get_caiwu:
    def __init__(self,name,path,codeList):
        self.name = name
        self.codeList = codeList
        self.path = path+'\\'+name
        self.path2 = path +'\\'+name+'_factor'
        try:
            os.chdir(self.path)
            print(self.path + ' existed')
        except:
            os.makedirs(self.path)
            print(self.path + ' created')
            os.chdir(self.path)

    def get_online(self,code):
        time.sleep(0.1)
        try:
            url = 'https://quotes.money.163.com/service/'+self.name+'_%s.html'
            url = url % (code)
            df = pd.read_csv(url, encoding='gb2312')
            df.to_pickle(self.path +'\\' + code + '.pkl')
            return 1
        except:
            print(code + ' fail')
            return code

    def get_data(self):
        return list(map(self.get_online,self.codeList))

    def read_pkl(self,name):
        try:
            df = pd.read_pickle(name)
            df.columns = [x.strip() for x in df.columns]
            df.index = df.报告日期
            df = df.drop(['报告日期'],axis = 1).T.dropna().replace('--',0)
            df['code'] = name[:6]
            df['financialdate'] = df.index
            return df
        except:
            print(name + ' lost')
            return None

    def get_factor(self):
        nameList = os.listdir()
        try:
            os.makedirs(self.path2)
            print(self.path2 + ' created')
        except:
            print(self.path2 + ' existed')

        df = pd.concat(list(map(self.read_pkl,nameList)))
        print('factor to be saved')
        col = df.columns.to_list()
        col.remove('code')
        col.remove('financialdate')
        for i in col:
            tem = pd.pivot(df,index ='financialdate',columns = 'code',values=i)
            tem.to_pickle(self.path2+'\\'+i+'.pkl')
        return


if __name__ == '__main__':

    os.chdir(r'H:\data')
    df = pd.read_csv('20211028.csv',index_col = 0)
    codeList = [x[:6] for x in df.ts_code.to_list()]
    ansList = list(map(get_lrb,codeList))
    ansList_zcfzb = list(map(get_zcfzb,codeList))
    ansList_xjllb = list(map(get_xjllb,codeList))

    S = get_caiwu('lrb', 'H:\data', codeList)
    S.get_factor()
    zc = get_caiwu('zcfzb', 'H:\data', codeList)
    zc.get_factor()
    xjl = get_caiwu('xjllb', 'H:\data', codeList)
    xjl.get_factor()







# code = '601919'
# get_lrb(code)
# df =pd.read_pickle(r'H:\data\\'+code+'.pkl')

# import baostock as bs
# import pandas as pd
#
# # 登陆系统
# lg = bs.login()
# # 显示登陆返回信息
# print('login respond error_code:'+lg.error_code)
# print('login respond  error_msg:'+lg.error_msg)
#
# # 查询季频估值指标盈利能力
# profit_list = []
# rs_profit = bs.query_profit_data(code="sh.600000", year=2017, quarter=2)
# while (rs_profit.error_code == '0') & rs_profit.next():
#     profit_list.append(rs_profit.get_row_data())
# result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
# # 打印输出
# print(result_profit)
# # 结果集输出到csv文件
# result_profit.to_csv("D:\\profit_data.csv", encoding="gbk", index=False)
#
#
# rs_forecast = bs.query_forecast_report("sh.601919", start_date="2010-01-01", end_date="2021-11-18")
# print('query_forecast_reprot respond error_code:'+rs_forecast.error_code)
# print('query_forecast_reprot respond  error_msg:'+rs_forecast.error_msg)
# rs_forecast_list = []
# while (rs_forecast.error_code == '0') & rs_forecast.next():
#     # 分页查询，将每页信息合并在一起
#     rs_forecast_list.append(rs_forecast.get_row_data())
# result_forecast = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)
# #### 结果集输出到csv文件 ####
# result_forecast.to_csv(r"H:\forecast_report.csv", encoding="gbk", index=False)
# print(result_forecast)