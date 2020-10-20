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
from scipy.stats import norm

call_price_data=[]
time_data=[]

def call_hourly_data(s,k,iv,T):
    
    """Hourly Data of Call prices"""
    
    for i in range(0,T):
        
        T=T-1
        
        if(T>=0):
            
            t=(T/(365*24))
            time_data.append(i)
            
            v=iv*0.01
            d1= (np.log(s/k) + ((0.1 +(v*v*0.5))*t)) / (v*np.sqrt(t))
            d2=d1-(v*np.sqrt(t))
        
            phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
    
            callprice= (s*norm.cdf(d1)) - k*norm.cdf(d2)*np.exp(-0.1*t)
            call_price_data.append(callprice)

    return 

call_hourly_data(9800,9900,25,100)

call_price_data=pd.DataFrame(call_price_data)
time_data=pd.DataFrame(time_data)
data_hourly=pd.concat([time_data,call_price_data], axis=1)
data_hourly.columns=['Hour_left','Call_price']
#data_hourly=data_hourly.set_index(data_hourly['Hour_left'])
#data_hourly=data_hourly[['Call_price']]
sns.set(style='whitegrid')
plt.figure(figsize=(18,8))
plt.title("Hourly_call_price")
plt.plot(data_hourly['Hour_left'],data_hourly['Call_price'],color='green')
plt.ylabel("Price of call option")
plt.xlabel("Hour left")
plt.show()

call_price_data=[]
time_data=[]

def call_minute_data(s,k,iv,T):
    
    T=T*60
    """Minute data of Call prices"""
    
    for i in range(0,T):
        
        T=T-1
        
        if(T>=0):
            
            t=(T/(365*1440))
            time_data.append(i)
            
            v=iv*0.01
            d1= (np.log(s/k) + ((0.1 +(v*v*0.5))*t)) / (v*np.sqrt(t))
            d2=d1-(v*np.sqrt(t))
        
            phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
    
            callprice= (s*norm.cdf(d1)) - k*norm.cdf(d2)*np.exp(-0.1*t)
            call_price_data.append(callprice)

    return 

call_minute_data(11485,11550,23,11)

call_price_data=pd.DataFrame(call_price_data)
time_data=pd.DataFrame(time_data)
data_hourly=pd.concat([time_data,call_price_data], axis=1)
data_hourly.columns=['Minutes_left','Call_price']
#data_hourly=data_hourly.set_index(data_hourly['Hour_left'])
#data_hourly=data_hourly[['Call_price']]
sns.set(style='whitegrid')
plt.figure(figsize=(18,8))
plt.title("Minutes_left_call_price")
plt.plot(data_hourly['Minutes_left'],data_hourly['Call_price'], color='black')
plt.ylabel("Price of call option")
plt.xlabel("Minutes left")
plt.show()


call_price_data=[]
time_data=[]

def call_seconds_data(s,k,iv,T):
    
    T=T*3600
    """Seconds data of Call prices"""
    
    for i in range(0,T):
        
        T=T-1
        
        if(T>=0):
            
            t=(T/(365*86400))
            time_data.append(i)
            
            v=iv*0.01
            d1= (np.log(s/k) + ((0.1 +(v*v*0.5))*t)) / (v*np.sqrt(t))
            d2=d1-(v*np.sqrt(t))
        
            phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
    
            callprice= (s*norm.cdf(d1)) - k*norm.cdf(d2)*np.exp(-0.1*t)
            call_price_data.append(callprice)

    return 

call_seconds_data(9800,9900,25,100)

call_price_data=pd.DataFrame(call_price_data)
time_data=pd.DataFrame(time_data)
data_hourly=pd.concat([time_data,call_price_data], axis=1)
data_hourly.columns=['seconds_left','Call_price']
#data_hourly=data_hourly.set_index(data_hourly['Hour_left'])
#data_hourly=data_hourly[['Call_price']]
sns.set(style='whitegrid')
plt.figure(figsize=(18,8))
plt.title("Seconds_left_call_price")
plt.plot(data_hourly['seconds_left'],data_hourly['Call_price'], color='red')
plt.ylabel("Price of call option")
plt.xlabel("Seconds left")
plt.show()