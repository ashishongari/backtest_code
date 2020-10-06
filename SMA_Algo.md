import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
%matplotlib inline
import pandas_datareader as pdr
import datetime 
import yfinance as yf
from nsepy import get_history
from datetime import date
import datetime as dt
from nsetools import Nse 

def moving_avg(symbol,n):
    
    """Moving avg eod backtest"""
    
    stock = pdr.get_data_yahoo(symbol, start="2009-01-01", end=date.today())['Close']
    stock=pd.DataFrame(stock)
    stock.columns=['Close'] 
    
    stock['avg'] = stock.Close.shift(0).rolling(window=n).mean()
    
    stock['long_entry'] = stock.Close > stock.avg
    stock['short_entry'] = stock.Close < stock.avg
    
    stock['long_exit'] = stock.Close < stock.avg
    stock['short_exit'] = stock.Close > stock.avg
    
    stock['positions_long'] = np.nan 
    stock.loc[stock.long_entry,'positions_long']= 1 
    stock.loc[stock.long_exit,'positions_long']= 0 
    
    stock['positions_short'] = np.nan 
    stock.loc[stock.short_entry,'positions_short']= -1 
    stock.loc[stock.short_exit,'positions_short']= 0 
    
    stock['Signal'] = stock.positions_long + stock.positions_short 

    stock = stock.fillna(method='ffill')
    
    stock['Signal']=stock['Signal'].shift(1)
    stock.dropna()
    
    daily_log_returns = np.log(stock.Close/stock.Close.shift(1)) 
    daily_log_returns = daily_log_returns * stock.Signal.shift(1) 
    daily_log_returns=daily_log_returns.dropna()
    daily_log_returns=np.array(daily_log_returns)
    
    sum=100
    portfolio=[]
    for i in range(len(daily_log_returns)):
        sum=sum*(1+daily_log_returns[i])
        portfolio.append(sum)
    
    portfolio=pd.DataFrame(portfolio)
    portfolio.columns=['Portfolio']
    
    #portfolio.plot()
    sns.set(style='whitegrid')
    plt.figure(figsize=(18,8))
    plt.title("Portofolio Cummulative return of Moving Average")
    #print(stock.index)
    
    return plt.plot(portfolio['Portfolio'])

moving_avg('^NSEBANK',15)
