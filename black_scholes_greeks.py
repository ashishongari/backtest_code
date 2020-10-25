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


#VEGA CALCULATION CODE
vegastrike=[]
vstrikepoint=[]

def vegastrikeloop(vstrikepoint,vegastrike,s,k,r,iv,T,strike):
    
    for i in range(strike):
        s=s+50
        vstrikepoint.append(s)
        t=T/365
        r=r*0.01
        v=iv*0.01
        d1= (np.log(s/k) + ((r +(v*v*0.5))*t)) / (v*np.sqrt(t))
        d2=d1-(v*np.sqrt(t))
        phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
        vega=s*phi*np.sqrt(t)
        vega=round(vega/100,4)
        vegastrike.append(vega)
        
    return 
        
vegastrikeloop(vstrikepoint,vegastrike,7800,10000,10,40,5,100)

vegastrike=np.array(vegastrike)
vstrikepoint=np.array(vstrikepoint)
plt.figure(figsize=(20,8))
plt.style.use('seaborn-darkgrid')
plt.plot(vstrikepoint,vegastrike, color="black")
plt.title("Vega at Different Strike")
plt.show()

#GAMMA CALCULATION CODE
gammastrike=[]
gstrikepoint=[]

def gammastrikeloop(gstrikepoint,gammastrike,s,k,iv,T):
    
    for i in range(100):
        s=s+50
        gstrikepoint.append(s)
        t=T/365
        r=0.1
        v=iv*0.01
        d1= (np.log(s/k) + ((r +(v*v*0.5))*t)) / (v*np.sqrt(t))
        d2=d1-(v*np.sqrt(t))
        phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
        gamma=phi/(s*v*t)
        gamma=round(gamma,4)
        gammastrike.append(gamma)
        
    return 

gammastrikeloop(gstrikepoint,gammastrike,8500,11350,23,7)

gammastrike=np.array(gammastrike)
gstrikepoint=np.array(gstrikepoint)
plt.figure(figsize=(20,8))
plt.style.use('seaborn-darkgrid')
plt.plot(gstrikepoint,gammastrike, color="red")
plt.title("Gamma at Different Strike")
plt.show()

thetastrike=[]
tstrikepoint=[]

def thetastrikeloop(tstrikepoint,thetastrike,s,k,r,iv,T,n):
    
    for i in range(n):
        s=s+50
        tstrikepoint.append(s)
        t=T/365
        r=r*0.01
        v=iv*0.01
        d1= (np.log(s/k) + ((r +(v*v*0.5))*t)) / (v*np.sqrt(t))
        d2=d1-(v*np.sqrt(t))
        phi=np.exp(-d1*d1*0.5)/np.sqrt(2*np.pi)
        theta= (-(s*phi*v/2*np.sqrt(t))) + (r*k*np.exp(-t*r)*norm.cdf(-d2))
        theta=round(theta/100, 4)
        thetastrike.append(theta)
        
    return 
        
thetastrikeloop(tstrikepoint,thetastrike,17000,18000,10,15,2,38)

thetastrike=np.array(thetastrike)
tstrikepoint=np.array(tstrikepoint)
plt.figure(figsize=(20,8))
plt.style.use('seaborn-darkgrid')
plt.plot(tstrikepoint[2:len(tstrikepoint)],thetastrike[2:len(thetastrike)], color="green")
plt.title("Theta at Different Strike")
plt.show()