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

#PUT OPTIONS GREEKS AND PRICE
def put(s,k,r,iv,T):

    t=T/(365*24)
    r=r*0.01
    v=iv*0.01
    d1= (np.log(s/k) + ((r +(v*v*0.5))*t)) / (v*np.sqrt(t))
    d2=d1-(v*np.sqrt(t))
    delta=norm.cdf(d1)-1
    delta=round(delta,4)
    phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
    gamma=phi/(s*v*t)
    gamma=round(gamma,4)
    vega=s*phi*np.sqrt(t)
    vega=round(vega/100,4)
    theta= (-(s*phi*v/2*np.sqrt(t))) + (r*k*np.exp(-t*r)*norm.cdf(-d2))
    theta=round(theta/100, 4)
    putprice= (-s*norm.cdf(-d1)) + k*norm.cdf(-d2)*np.exp(-r*t)
    print("Price of Put option is :",str(round(putprice,2)))
    print("Delta is :",str(delta))
    print("Gamma is :", str(gamma))
    print("Vega is :", str(vega))
    print('Theta is :', str(theta))
    
    return 

put(9450,9400,10,69.9,100)

#CALL OPTIONS GREEKS AND PRICE

def call(s,k,r,iv,T):
    t=T/365
    r=r*0.01
    v=iv*0.01
    d1= (np.log(s/k) + ((r +(v*v*0.5))*t)) / (v*np.sqrt(t))
    d2=d1-(v*np.sqrt(t))
    phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
    vega=s*phi*np.sqrt(t)
    vega=round(vega/100,4)
    theta= (-(s*phi*v/2*np.sqrt(t))) - (r*k*np.exp(-t*r)*norm.cdf(-d2))
    theta=round(theta/100, 4)
    callprice= (s*norm.cdf(d1)) - k*norm.cdf(d2)*np.exp(-r*t)
    print("Vega is :", str(vega))
    print('Theta is :', str(theta))

    return callprice

call(10000,10000,10,60,5)