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
import talib

"""
Create a class named stock 
"""

class stock:
    
    def __init__(self,symbol,):
        
        self.symbol=symbol
  
    def historical_data(self):
        
        df=pdr.get_data_yahoo(self.symbol, start=datetime.datetime(2010, 1, 1), end=datetime.datetime.today())['Adj Close']
        
        return df

def WILLIAMS(period,lot_size):

    """
    Use Yahoo Finance Ticker symbol to pull data for a particular stocks
    """
    
    df=stock('^NSEI')
    df=df.historical_data()
    df=df[['High','Low','Adj Close']]
    
    """
    Plot and define William'sR% Indicator
    """
    
    wri= talib.WILLR(df['High'], df['Low'], df['Adj Close'], timeperiod=period)
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(wri, color='maroon')
    plt.title(f"WILLR - Williams' %R")
    
    """
    make a datframe for backtest
    """
    
    df_backtest=pd.concat([df['Adj Close'], wri], axis=1)
    df_backtest.columns=['close','William']
    df_backtest['prev_close']=df_backtest['close'].shift(1)
    df_backtest['change'] = df_backtest['close'].sub(df_backtest['prev_close'])
    df_backtest = df_backtest.dropna()
    
    """
    Define logic for buy entry and exit
    """
    
    df_backtest['william_signal_buy_entry']=np.where( df_backtest['William'] <=-80 ,1,0)

    df_backtest['buy_exit']=np.where( df_backtest['William'] >=-20 ,1,0)

    df_backtest['buy_position']=0

    for i in range(len(df_backtest)):
        
        if (df_backtest['william_signal_buy_entry'].iloc[i] ==0 and df_backtest['buy_exit'].iloc[i] ==1) and (df_backtest['buy_position'].iloc[i-1] =='postion_live'):
            
            df_backtest['buy_position'].iloc[i]='no_position'
        
        elif (df_backtest['william_signal_buy_entry'].iloc[i] ==1 and df_backtest['buy_exit'].iloc[i] ==0) or (df_backtest['buy_position'].iloc[i-1] =='postion_live') :
            
            df_backtest['buy_position'].iloc[i]='postion_live'
            
        else :
            
            df_backtest['buy_position'].iloc[i]='no_position'

    """
    Define logic for sell  entry and exit
    """
    
    df_backtest['william_signal_sell_entry']=np.where( df_backtest['William']  >=-20,1,0)

    df_backtest['sell_exit']=np.where( df_backtest['William'] <=-80 ,1,0)

    df_backtest['sell_position']=0

    for i in range(len(df_backtest)):
        
        if (df_backtest['william_signal_sell_entry'].iloc[i] ==0 and df_backtest['sell_exit'].iloc[i] ==1) and (df_backtest['sell_position'].iloc[i-1] =='postion_live'):
            
            df_backtest['sell_position'].iloc[i]='no_position'
        
        elif (df_backtest['william_signal_sell_entry'].iloc[i] ==1 and df_backtest['sell_exit'].iloc[i] ==0) or (df_backtest['sell_position'].iloc[i-1] =='postion_live') :
            
            df_backtest['sell_position'].iloc[i]='postion_live'
            
        else :
            
            df_backtest['sell_position'].iloc[i]='no_position'

    """
    Generate final signal for buy,sell and exit 
    """
            

    df_backtest['buy_signal']=np.where(df_backtest['buy_position'] =='postion_live', 1 , 0)
    df_backtest['sell_signal']=np.where(df_backtest['sell_position'] =='postion_live', -1 , 0)
    df_backtest['signal']= df_backtest['buy_signal'].add(df_backtest['sell_signal'])
    
    """
    run logic for equity curve of backtest with intial margin as 8,00,000
    """

    df_backtest['Portfolio_Margin']=0

    for i in range(len(df_backtest)):
        
        if i==0:
            
            df_backtest['Portfolio_Margin'].iloc[i] =8_00_000
    
        elif df_backtest['signal'].iloc[i] ==1:
            
            df_backtest['Portfolio_Margin'].iloc[i] =df_backtest['Portfolio_Margin'].iloc[i-1] + (df_backtest['change'].iloc[i]*lot_size)
        
        elif df_backtest['signal'].iloc[i] ==-1:
            
            df_backtest['Portfolio_Margin'].iloc[i] =df_backtest['Portfolio_Margin'].iloc[i-1] + (-1*df_backtest['change'].iloc[i]*lot_size)
        
        else:
            
            df_backtest['Portfolio_Margin'].iloc[i] =df_backtest['Portfolio_Margin'].iloc[i-1]

    """
    Plot the equity curve
    """
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot( df_backtest['Portfolio_Margin'], color='green')
    plt.title(f"Williams %R  indicator backtest with {period} period")
    
    
    return df_backtest.tail()

WILLIAMS(15,75)
