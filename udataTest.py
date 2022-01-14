from hs_udata import set_token,stock_list,trading_calendar  ,schedule_disclosure   # 引入hs_udata模块中set_token和stock_list
set_token(token = '100wMtAhxx_eBsaLgp1fyVDblzoOTA7XUzeY5m_0ng1kvvtMHivO28LGTQguQPa1')        # 设置Token
data = stock_list()
codeStr = ','.join(data.hs_code.values)
schedule = schedule_disclosure(en_prod_code=codeStr[:1969],report_date="2019-12-31,2020-12-31")# 获取 股票列表数据，返回格式为dataframe
print(data.head())

