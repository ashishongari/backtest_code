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

class stat_arb:
    
    def __init__(self,sy_1, sy_2):
        
        self.sy_1=sy_1
        self.sy_2=sy_2
        
    def historical_data(self):
        
        x=pdr.get_data_yahoo(self.sy_1, start=datetime.datetime(2010, 4, 1), end=datetime.datetime.today())['Adj Close']
        y=pdr.get_data_yahoo(self.sy_2, start=datetime.datetime(2010, 4, 1), end=datetime.datetime.today())['Adj Close']
        
        df_stat=pd.concat([x,y], axis=1)
        df_stat.columns=['x','y']
        
        df_stat=df_stat.dropna()
        
        return df_stat

pair_1=stat_arb('INFY.NS','TCS.NS')
pair_1=pair_1.historical_data()
# print(pair_1)

from nsetools import Nse 
nse = Nse()
lot_size_dict=nse.get_fno_lot_sizes()

"""
Co-Interagtion Test 

"""
lot_size_x=lot_size_dict['INFY']
lot_size_y=lot_size_dict['TCS']

pair_1=stat_arb('INFY.NS','TCS.NS')
pair_1=pair_1.historical_data()

model_1 =sm.OLS(pair_1.y.iloc[:len(pair_1)-1], pair_1.x.iloc[:len(pair_1)-1])
model_1=model_1.fit()
hedgeratio_1=model_1.params[0]

pair_1['spread']=pair_1.y-(hedgeratio_1*pair_1.x)

pair_1.spread.plot(figsize=(8,5))
adf=adfuller (pair_1.spread, maxlag=1)

print(adf[0])
print(adf[4])


"""
Backtest_code of pair
"""

pair_1['ma']=pair_1['spread'].rolling(window=10).mean()
pair_1['std']=pair_1['spread'].rolling(window=10).std()

pair_1['zscore']=(pair_1['spread'].sub(pair_1['ma'])).div(pair_1['std'])

pair_1['zscore']=round(pair_1['zscore'],2)

pair_1=pair_1.copy().dropna()


"""
BUY AND EXIT LOGIC
"""

pair_1['z_signal_buy_entry']=np.where( pair_1['zscore'] >=1.75,1,0)

pair_1['buy_exit']=np.where( pair_1['zscore'] <0 ,1,0)

pair_1['buy_position']=0

for i in range(len(pair_1)):
    
    if (pair_1['z_signal_buy_entry'].iloc[i] ==0 and pair_1['buy_exit'].iloc[i] ==1) and (pair_1['buy_position'].iloc[i-1] =='postion_live'):
        
        pair_1['buy_position'].iloc[i]='no_position'
        
    elif (pair_1['z_signal_buy_entry'].iloc[i] ==1 and pair_1['buy_exit'].iloc[i] ==0) or (pair_1['buy_position'].iloc[i-1] =='postion_live') :
        
         pair_1['buy_position'].iloc[i]='postion_live'
            
    else :
        
        pair_1['buy_position'].iloc[i]='no_position'

        
"""
SELL AND EXIT LOGIC 
"""

pair_1['z_signal_sell_entry']=np.where( pair_1['zscore']  <=-1.75,1,0)

pair_1['sell_exit']=np.where( pair_1['zscore'] >0 ,1,0)

pair_1['sell_position']=0


for i in range(len(pair_1)):
    
    if (pair_1['z_signal_sell_entry'].iloc[i] ==0 and pair_1['sell_exit'].iloc[i] ==1) and (pair_1['sell_position'].iloc[i-1] =='postion_live'):
        
        pair_1['sell_position'].iloc[i]='no_position'
        
    elif (pair_1['z_signal_sell_entry'].iloc[i] ==1 and pair_1['sell_exit'].iloc[i] ==0) or (pair_1['sell_position'].iloc[i-1] =='postion_live') :
        
         pair_1['sell_position'].iloc[i]='postion_live'
            
    else :
        
        pair_1['sell_position'].iloc[i]='no_position'
        
"""
FINAL BUY & SELL SIGNAL
"""
pair_test=pair_1.copy()
pair_test=pair_test[['zscore','x','y','buy_position','sell_position']]

pair_test['upper_signal']=np.where( pair_test['buy_position']=='postion_live', 1 , 0)
pair_test['lower_signal']=np.where( pair_test['sell_position']=='postion_live', -1 , 0)

pair_test['final_signal']=pair_test['upper_signal'].add(pair_test['lower_signal'])

pair_test['x_prev']=pair_test['x'].shift(1)
pair_test['y_prev']=pair_test['y'].shift(1)

pair_test['x_diff']=pair_test['x'].sub(pair_test['x_prev'])
pair_test['y_diff']=pair_test['y'].sub(pair_test['y_prev'])

pair_test=pair_test[['zscore','x_diff','y_diff','final_signal']]

#################################################################################

# pair_test['final_signal']=pair_test['final_signal'].shift(1)

#################################################################################
pair_test=pair_test.dropna()

pair_test['x_cum_short_upper_zscore']=0
pair_test['y_cum_long_upper_zcore']=0


for i in range(len(pair_1)-1):
    
    if pair_test['final_signal'].iloc[i]==1:
        
        pair_test['x_cum_short_upper_zscore'].iloc[i] = -(pair_test['x_diff'].iloc[i]*lot_size_x)
        pair_test['y_cum_long_upper_zcore'].iloc[i] = pair_test['y_diff'].iloc[i]*lot_size_y
        
    else:
        pair_test['x_cum_short_upper_zscore'].iloc[i]=0
        pair_test['y_cum_long_upper_zcore'].iloc[i]=0
        
        
pair_test['upper_zscore_mtm']=pair_test['x_cum_short_upper_zscore'] + pair_test['y_cum_long_upper_zcore']

pair_test['x_cum_long_lower_zscore']=0
pair_test['y_cum_short_lower_zcore']=0



for i in range(len(pair_1)-1):
    
    if pair_test['final_signal'].iloc[i]==-1:
        
        pair_test['x_cum_long_lower_zscore'].iloc[i] = pair_test['x_diff'].iloc[i]*lot_size_x
        pair_test['y_cum_short_lower_zcore'].iloc[i] = -(pair_test['y_diff'].iloc[i]*lot_size_y)
        
    else:
        pair_test['x_cum_long_lower_zscore'].iloc[i]=0
        pair_test['y_cum_short_lower_zcore'].iloc[i]=0


pair_test['lower_zscore_mtm']=pair_test['x_cum_long_lower_zscore'] + pair_test['y_cum_short_lower_zcore']   

pair_test=pair_test[['zscore','final_signal','upper_zscore_mtm','lower_zscore_mtm']]

pair_test['mtm']=pair_test['upper_zscore_mtm'] + pair_test['lower_zscore_mtm']

pair_test['Portfolio_Margin']=0

for i in range(len(pair_test)):
    
    if i==0:
        
        pair_test['Portfolio_Margin'].iloc[i]=8_00_000
        
    else:
        
        pair_test['Portfolio_Margin'].iloc[i]=(pair_test['Portfolio_Margin'].iloc[i-1]+pair_test['mtm'].iloc[i])-100
        

pair_test['total_trade']=0
     
for i in range(len(pair_test)):
    
    if pair_test['final_signal'].iloc[i] != pair_test['final_signal'].iloc[i-1]:
        
        pair_test['total_trade'].iloc[i] = pair_test['total_trade'].iloc[i-1] + 1
    else:
         pair_test['total_trade'].iloc[i] =  pair_test['total_trade'].iloc[i-1]

        
pair_test['slippage']=0

for i in range(len(pair_test)):
    
    if pair_test['total_trade'].iloc[i] != pair_test['total_trade'].iloc[i-1]:
        
        pair_test['slippage'].iloc[i] =  -1600
    else:
         pair_test['slippage'].iloc[i] = 0


plt.figure(figsize=(20,10))
sns.set(style="whitegrid")
plt.plot(pair_test['Portfolio_Margin'].iloc[1:len(pair_test)], color='green')
plt.title("CUMMULATIVE PL")
    

window = 252
Roll_Max_portfolio = pair_test['Portfolio_Margin'].iloc[1:len(pair_test)].rolling(window, min_periods=1).max()
Daily_Drawdown_portfolio = (pair_test['Portfolio_Margin'].iloc[1:len(pair_test)]/Roll_Max_portfolio - 1)*100

# Plot the results
plt.figure(figsize=(20,8))
plt.plot(Daily_Drawdown_portfolio, color="red", label="PORTFOLIO")
plt.title("DRAWDOWN")
plt.legend()
plt.show()

print(f"Total Slippage is {pair_test['slippage'].sum()}")

pair_test.tail()