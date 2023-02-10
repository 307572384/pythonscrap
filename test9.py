import pandas as pd
import numpy as np
import tushare as ts
import alphalens

ts.set_token('7f66bf5cc1540c22428dcb17dc8d5487fdb3c759f6a3340365610efd')
pro = ts.pro_api()
wdays = pro.trade_cal(exchange_id='', start_date='20180101', end_date='20180231')
wdays = wdays[wdays.is_open==1].cal_date.values.tolist()
factors_list = []
for idate in wdays :
    temp_df = pro.query('daily',ts_code='', trade_date=idate)
    factors_list.append(temp_df)
factor_df = pd.concat(factors_list)
def worker(iticker):
    print(iticker)
    temp_quote = None
    try:
        ticker = iticker.split('.')[0]
        temp_quote = ts.get_k_data(ticker,start='2018-01-01',end='2018-02-31',autype = 'qfq').loc[:,['date','close']]
        temp_quote['ts_code'] = iticker
        return temp_quote
    except:
        return None

quote_list = []
tickers = list(set(factor_df.ts_code))

from multiprocessing import Pool
pool = Pool(8)
res = pool.map(worker,tickers)
quotes = pd.concat(res)
quotes.rename(columns={'date':'trade_date'},inplace=True)
factor_df.trade_date = pd.to_datetime(factor_df.trade_date.astype('str'))
quotes.trade_date = pd.to_datetime(quotes.trade_date)
factor = factor_df.loc[:,['ts_code','trade_date','ps_ttm']].set_index(['trade_date','ts_code'])
factor = factor.unstack().fillna(method='ffill').stack()
prices = quotes.pivot(index='trade_date',columns='ts_code',values='close')
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(
    factor,
    prices,
    groupby=None,
    quantiles=5,
    periods=(10,20,40),
    filter_zscore=None)
mean_return_by_q_daily, std_err = alphalens.performance.mean_return_by_quantile(factor_data, by_date=True)
mean_return_by_q, std_err_by_q = alphalens.performance.mean_return_by_quantile(factor_data, by_date=False)
alphalens.plotting.plot_quantile_returns_bar(mean_return_by_q)
