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
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm  

from nsetools import Nse 
nse = Nse()
lot_size_dict=nse.get_fno_lot_sizes()

ticker='FEDERALBNK'

lot_size=lot_size_dict[ticker]

data = pdr.get_data_yahoo('FEDERALBNK.NS', start=datetime.datetime(2011, 1, 1), end=datetime.datetime.today())['Close']
data=pd.DataFrame(data)

data['prev_Close']=data['Close'].shift(1)
data['running_min']=data['Close'].expanding().max()
data['point_change']=data['Close'].sub(data['prev_Close'])

data['Change']=((data['Close'].div(data['running_min']))-1)*100
data['short_sell']=-50.0
data['exit']=-40.0

plt.figure(figsize=(18,8))
data['Change'].plot()
data['short_sell'].plot()
data['exit'].plot()

data['short_sell_signal']=data['Change']<-50.0
data['exit_signal']=data['Change']>-40.0
data['signal']=0


for i in range(len(data)):
    
    if i==0:
        data['signal'].iloc[i]='No_Position'
        
    elif data['short_sell_signal'].iloc[i]==True and data['exit_signal'].iloc[i]==False:
        
        data['signal'].iloc[i]='Short_sell'
        
    else:
        
        data['signal'].iloc[i]='No_Position'  


data['MTM']=0

data['signal']=data['signal'].shift(1)

for i in range(len(data)):
    
    if i==0:
        
        data['MTM']=0
    
    elif data['signal'].iloc[i]=='Short_sell':
        
        data['MTM'].iloc[i]=(-data['point_change'].iloc[i]*lot_size)-5
        
    else:
        
        data['MTM'].iloc[i]=0
        
data['Portfolio_Margin']=0

for i in range(len(data)):
    
    if i==0:
        data['Portfolio_Margin'].iloc[i]=8_00_000
        
    else:
        
        data['Portfolio_Margin'].iloc[i]=data['Portfolio_Margin'].iloc[i-1]+data['MTM'].iloc[i-1]
     
plt.figure(figsize=(18,8))
plt.plot(data['Portfolio_Margin'], color='green')
plt.title("Equity Curve")
plt.show()