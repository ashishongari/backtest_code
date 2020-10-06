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

"""
short sell a stock when the drawdown is more than 50%
and exit when drawdown is less than 37.5%

"""

"""
Get ticker data from Yahoo Finance EOD

"""

ticker='INDUSINDBK'

lot_size=800

data = pdr.get_data_yahoo('INDUSINDBK.NS', start=datetime.datetime(2011, 1, 1), end=datetime.datetime.today())['Close']
data=pd.DataFrame(data)

"""
Put the short sell conditon
"""

data['prev_Close']=data['Close'].shift(1)
data['running_min']=data['Close'].expanding().max()
data['point_change']=data['Close'].sub(data['prev_Close'])

data['Change']=((data['Close'].div(data['running_min']))-1)*100
data['short_sell']=-50.0
data['exit']=-37.5

"""
plot the drawdown chart

"""

plt.figure(figsize=(18,8))
data['Change'].plot()
data['short_sell'].plot()
data['exit'].plot()

data['short_sell_signal']=data['Change']<-50.0
data['exit_signal']=data['Change']>-37.5
data['signal']=0


""""
Generate the short sell and exit signal
"""

for i in range(len(data)):
    
    if i==0:
        data['signal'].iloc[i]='No_Position'
        
    elif data['short_sell_signal'].iloc[i]==True and data['exit_signal'].iloc[i]==False:
  
        data['signal'].iloc[i]='Short_sell'
        
    else:
        
        data['signal'].iloc[i]='No_Position'  
        
    data['signal']=data['signal'].shift(1)


data['MTM']=0

"""
Calculate the MTM value

"""

for i in range(len(data)):
    
    if i==0:
        
        data['MTM'].iloc[i]=0
    
    elif data['signal'].iloc[i]=='Short_sell':
        
        data['MTM'].iloc[i]=(-data['point_change'].iloc[i]*lot_size)-5
        
    else:
        
        data['MTM'].iloc[i]=0
        
data['Portfolio_Margin']=0


"""
calculate the overall loss/gain on overall portfolio as 8_00_000 as starting margin

"""

for i in range(len(data)):
    
    if i==0:
        data['Portfolio_Margin'].iloc[i]=8_00_000
        
    else:
        
        data['Portfolio_Margin'].iloc[i]=data['Portfolio_Margin'].iloc[i-1]+data['MTM'].iloc[i-1]
     
"""
plot the equity curve

"""
plt.figure(figsize=(18,8))
plt.plot(data['Portfolio_Margin'], color='green')
plt.title("Equity Curve")
