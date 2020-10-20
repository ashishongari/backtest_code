import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import pandas_datareader as pdr
import datetime 
import yfinance as yf
from nsepy import get_history
from datetime import date
import datetime as dt
from nsetools import Nse
import talib
import seaborn as sns

class stock:
    
    def __init__(self,symbol,):
        
        self.symbol=symbol
  
    def historical_data(self):
        
        df=pdr.get_data_yahoo(self.symbol, start=datetime.datetime(2008, 1, 1), end=datetime.datetime.today())[['Open','High', 'Low','Adj Close']]
        
        return df



df=stock('^NSEI')
df=df.historical_data()
df= df['Adj Close']
print(df)

def WILLIAMS(period,lot_size):
    
    df=stock('^NSEI')
    df=df.historical_data()
    df=df[['High','Low','Adj Close']]

    wri= talib.WILLR(df['High'], df['Low'], df['Adj Close'], timeperiod=period)
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(wri, color='maroon')
    plt.title(f"WILLR - Williams' %R")
    plt.show()
    
    df_backtest=pd.concat([df['Adj Close'], wri], axis=1)
    df_backtest.columns=['close','William']
    df_backtest['prev_close']=df_backtest['close'].shift(1)
    df_backtest['change'] = df_backtest['close'].sub(df_backtest['prev_close'])
    df_backtest = df_backtest.dropna()

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


            

    df_backtest['buy_signal']=np.where(df_backtest['buy_position'] =='postion_live', 1 , 0)
    df_backtest['sell_signal']=np.where(df_backtest['sell_position'] =='postion_live', -1 , 0)
    df_backtest['signal']= df_backtest['buy_signal'].add(df_backtest['sell_signal'])

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

    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot( df_backtest['Portfolio_Margin'], color='green')
    plt.title(f"Williams %R  indicator backtest with {period} period")
    plt.show()
    
    return df_backtest.tail()

WILLIAMS(15,75)