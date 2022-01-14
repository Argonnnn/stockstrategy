import os
import pandas as pd
import datetime as dt
from hs_udata import set_token,financial_balance,stock_list,schedule_disclosure
set_token(token = 'lj-oYG8DPkvbNbqUvUwE-8YWlSQ5WzMeI7GAzzSScfh97jva8D4_FTghBHrwPxNO')

stocks = stock_list(listed_state = "1")
stockStr = ','.join(stocks.hs_code.values)
data = schedule_disclosure(en_prod_code=stockStr[4000:9999],report_date="2020-12-31")
data = financial_balance(secu_code="601919.SH,000001.SZ",
                         start_date="2011-01-01",end_date="2021-12-09")
print(data.end_date)


from hs_udata import set_token,leader_profile
set_token(token = '100wMtAhxx_eBsaLgp1fyVDblzoOTA7XUzeY5m_0ng1kvvtMHivO28LGTQguQPa1')

data = leader_profile(secu_code = "600570")
print(data.T)

from hs_udata import set_token,stock_quote_minutes

data = stock_quote_minutes(en_prod_code="000001.SZ",
                          begin_date="20210805",end_date="20210809")
print(data.head())