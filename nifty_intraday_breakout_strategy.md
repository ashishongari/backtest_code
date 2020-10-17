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

#Keep first 1 hour high and low as reference point
#Go long when spot goes above 1st Hour high and exit when it breaches  1st Hour low
#Go Short when spot goes above 1st Hour low and exit when it breaches  1st Hour High


"""
Use nifty intraday data for backtest 
"""

tick_data=pd.read_csv(r"C:\Users\............\Quantitative Research\Trading Research\nifty20152020.csv",parse_dates=True)
tick_data_test=tick_data[['Date','Time','Close']]

tick_data_test=tick_data_test.dropna()

tick_data_close=tick_data_test[['Date','Time','Close']]

date_date=tick_data_close['Date'].unique()

"""
Define a function for backtest
"""

mtm_array=[]

def nifty_intraday(lot_size, num_of_day):
    
    for i in range(num_of_day):
        
        tick_data_test_test=tick_data_test.loc[tick_data_test['Date']==date_date[i]]
        tick_data_test_test

        first_hour_high=tick_data_test_test['Close'].iloc[0:60].max()
        first_hour_low=tick_data_test_test['Close'].iloc[0:60].min()

        live_data=tick_data_test_test['Close'].iloc[61:len(tick_data_test_test)-1]
        live_data=pd.DataFrame(live_data)
        live_data['High']=first_hour_high
        live_data['Low']=first_hour_low

        live_data['prev_close']=live_data['Close'].shift(1)
        live_data['diff']=live_data['Close'].sub(live_data['prev_close'])


        live_data['signal_buy_entry']=np.where( live_data['Close'] > live_data['High']  ,1,0)

        live_data['buy_exit']=np.where( live_data['Close'] < live_data['Low']  ,1,0)

        live_data['buy_position']=0
        live_data=live_data.dropna()


        for i in range(len(live_data)-1):

            if (live_data['signal_buy_entry'].iloc[i] ==0 and live_data['buy_exit'].iloc[i] ==1) and (live_data['buy_position'].iloc[i-1] =='postion_live'):

                live_data['buy_position'].iloc[i]='no_position'

            elif (live_data['signal_buy_entry'].iloc[i] ==1 and live_data['buy_exit'].iloc[i] ==0) or (live_data['buy_position'].iloc[i-1] =='postion_live') :

                live_data['buy_position'].iloc[i]='postion_live'

            else :

                live_data['buy_position'].iloc[i]='no_position'



        live_data['signal_sell_entry']=np.where(live_data['Close'] < live_data['Low'],1,0)

        live_data['sell_exit']=np.where( live_data['Close'] > live_data['High'] ,1,0)

        live_data['sell_position']=0

        for i in range(len(live_data)-1):

            if (live_data['signal_sell_entry'].iloc[i] ==0 and live_data['sell_exit'].iloc[i] ==1) and (live_data['sell_position'].iloc[i-1] =='postion_live'):

                live_data['sell_position'].iloc[i]='no_position'

            elif (live_data['signal_sell_entry'].iloc[i] ==1 and live_data['sell_exit'].iloc[i] ==0) or (live_data['sell_position'].iloc[i-1] =='postion_live') :

                live_data['sell_position'].iloc[i]='postion_live'

            else :

                live_data['sell_position'].iloc[i]='no_position'


        live_data['buy_signal']=np.where(live_data['buy_position'] =='postion_live', 1 , 0)
        live_data['sell_signal']=np.where(live_data['sell_position'] =='postion_live', -1 , 0)
        live_data['signal']= live_data['buy_signal'].add(live_data['sell_signal'])


        live_data['MTM']=0

        for i in range(len(live_data)-1):

            if live_data['signal'].iloc[i] ==1:

                live_data['MTM'].iloc[i] =(live_data['diff'].iloc[i]*lot_size)

            elif live_data['signal'].iloc[i] ==-1:

                live_data['MTM'].iloc[i] =(-1*live_data['diff'].iloc[i]*lot_size)

            else:

                live_data['MTM'].iloc[i] =live_data['MTM'].iloc[i-1]

        mtm= live_data['MTM'].sum(axis=0)
        mtm_array.append(mtm)
         
    return
    
nifty_intraday(75,5)
