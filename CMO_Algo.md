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
        
 def CMO(period, lot_size):
    
    df=stock('^NSEI')
    df=df.historical_data()
    
    df['CMO']=talib.CMO(df['Adj Close'], timeperiod=period)
    
    """
    PLOT THE Commodity Channel Index of period
    """
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(df['CMO'])
    plt.title(f"Commodity Channel Index of period {period}")
    
    df_backtest=pd.concat([df['Adj Close'], df['CMO']], axis=1)
    df_backtest.columns=['close','cmo']
    df_backtest['prev_close']=df_backtest['close'].shift(1)
    df_backtest['change'] = df_backtest['close'].sub(df_backtest['prev_close'])
    df_backtest = df_backtest.dropna()
    
    """
    BUY  AND EXIT LOGIC (Buy when CMO goes below -50 and exit above 50)
    """
    df_backtest['cmo_signal_buy_entry']=np.where( df_backtest['cmo'] <= -50 ,1,0)

    df_backtest['buy_exit']=np.where( df_backtest['cmo'] >= 50 ,1,0)

    df_backtest['buy_position']=0

    for i in range(len(df_backtest)):
        
        if (df_backtest['cmo_signal_buy_entry'].iloc[i] ==0 and df_backtest['buy_exit'].iloc[i] ==1) and (df_backtest['buy_position'].iloc[i-1] =='postion_live'):
            
            df_backtest['buy_position'].iloc[i]='no_position'
        
        elif (df_backtest['cmo_signal_buy_entry'].iloc[i] ==1 and df_backtest['buy_exit'].iloc[i] ==0) or (df_backtest['buy_position'].iloc[i-1] =='postion_live') :
            
            df_backtest['buy_position'].iloc[i]='postion_live'
            
        else :
            
            df_backtest['buy_position'].iloc[i]='no_position'
   
    """
    SELL AND EXIT LOGIC (Buy when CMO goes above 50 and exit below -50)
    """
     
    df_backtest['cmo_signal_sell_entry']=np.where( df_backtest['cmo']  >= 50,1,0)

    df_backtest['sell_exit']=np.where( df_backtest['cmo'] <= -50 ,1,0)

    df_backtest['sell_position']=0


    for i in range(len(df_backtest)):
        
        if (df_backtest['cmo_signal_sell_entry'].iloc[i] ==0 and df_backtest['sell_exit'].iloc[i] ==1) and (df_backtest['sell_position'].iloc[i-1] =='postion_live'):
            
            df_backtest['sell_position'].iloc[i]='no_position'
        
        elif (df_backtest['cmo_signal_sell_entry'].iloc[i] ==1 and df_backtest['sell_exit'].iloc[i] ==0) or (df_backtest['sell_position'].iloc[i-1] =='postion_live') :
            
            df_backtest['sell_position'].iloc[i]='postion_live'
            
        else :
            
            df_backtest['sell_position'].iloc[i]='no_position'

    """
    FINAL BUY & SELL SIGNAL
    """
    df_backtest['buy_signal']=np.where(df_backtest['buy_position'] =='postion_live', 1 , 0)
    df_backtest['sell_signal']=np.where(df_backtest['sell_position'] =='postion_live', -1 , 0)
    df_backtest['signal']= df_backtest['buy_signal'].add(df_backtest['sell_signal'])
#     df_backtest['signal']=df_backtest['signal'].shift(1)
     
    """
    Starting portofolio with intial margin of Rs. 8,00,000  and lot size 75, equity is NIFTY FUTURES
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
    PLOT THE EQUITY CURVE OF BACKTEST
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot( df_backtest['Portfolio_Margin'], color='green')
    plt.title(f" Chande Momentum Oscillator backtest with {period} period")
    
    
    return 
                                      
CMO(14,75)
