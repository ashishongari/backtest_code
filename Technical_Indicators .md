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

class stock:
    
    def __init__(self,symbol,):
        
        self.symbol=symbol
  
    def historical_data(self):
        
        df=pdr.get_data_yahoo(self.symbol, start=datetime.datetime(2008, 1, 1), end=datetime.datetime.today())[['Open','High', 'Low','Adj Close']]
        
        return df
        
""""
Average Directional Movement Index
"""

def ADX(period):
   
    df_adx=stock('^NSEI')
    df_adx=df_adx.historical_data()
    df_adx=df_adx[['High','Low','Adj Close']]

    ti_adx= talib.ADX(df_adx['High'], df_adx['Low'], df_adx['Adj Close'], timeperiod=period)
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(ti_adx, color='red')
    plt.title(f"ADX - Average Directional Movement Index")
    
    return

ADX(14)

""""
Absolute Price Oscillator
"""

def APO():
    
    df_apo=stock('^DJI')
    df_apo=df_apo.historical_data()
    df_apo=df_apo['Adj Close']
    
    ti_apo =talib.APO(df_apo, fastperiod=12, slowperiod=26, matype=0)
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(ti_apo, color='purple')
    plt.title("APO - Absolute Price Oscillator")
    
    return

APO()

"""
Aroon Oscillator
""""
def AROONOSC(period):
    
    df_aroon=stock('^NSEI')
    df_aroon=df_aroon.historical_data()
    df_aroon=df_aroon[['High','Low']]
    
    tai_aroon=talib.AROONOSC( df_aroon['High'], df_aroon['Low'] , timeperiod=period)
    sns.set(style="whitegrid")
    plt.figure(figsize=(18,8))
    plt.plot(tai_aroon, color='blue')
    plt.title(f"AROONOSC - Aroon Oscillator of {period} period")
    
    return

AROONOSC(14)
