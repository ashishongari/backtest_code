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
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm  

tick_data_1=pd.read_csv(r"C:\Users\DeepakShenoy\Desktop\Quantitative Research\Trading Research\nifty20072014.csv",parse_dates=True, index_col=0)
tick_data_2 =pd.read_csv(r"C:\Users\DeepakShenoy\Desktop\Quantitative Research\Trading Research\nifty20152020.csv",parse_dates=True, index_col=0)

tick_data=pd.concat([ tick_data_1, tick_data_2])
tick_data_test=tick_data[['Date','Time','Close']]
tick_data_test=tick_data_test.dropna()

tick_data_test=tick_data[['Date','Time','Close']]
tick_data_test=tick_data_test.dropna()
tick_data_close=tick_data_test[['Date','Time','Close']]

date_date=tick_data_close['Date'].unique()
mtm_array=[]

print(tick_data_close)

def nifty_intraday(lot_size, num_of_day,candle):
    
    for i in range(num_of_day):
        
        tick_data_test_test=tick_data_test.loc[tick_data_test['Date']==date_date[i]]

        first_hour_high=tick_data_test_test['Close'].iloc[0:candle].max()
        first_hour_low=tick_data_test_test['Close'].iloc[0:candle].min()

        live_data=tick_data_test_test['Close'].iloc[candle+1:len(tick_data_test_test)-1]
        live_data=pd.DataFrame(live_data)
        live_data['High']=first_hour_high
        live_data['Low']=first_hour_low

        live_data['prev_close']=live_data['Close'].shift(1)
        live_data['diff']=live_data['Close'].sub(live_data['prev_close'])

        live_data['signal_buy_entry']=np.where( live_data['Close'] > live_data['High'] ,1,0)
        live_data['buy_exit']=np.where( live_data['Close'] < live_data['Low'] ,1,0)
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
        
        live_data['signal']=live_data['signal'].shift(1)

        live_data['MTM']=0

        for i in range(len(live_data)-1):

            if live_data['signal'].iloc[i] ==1:

                live_data['MTM'].iloc[i] =(live_data['diff'].iloc[i]*lot_size)

            elif live_data['signal'].iloc[i] ==-1:

                live_data['MTM'].iloc[i] =(-1*live_data['diff'].iloc[i]*lot_size)

            else:

                live_data['MTM'].iloc[i] =0

        mtm=live_data['MTM'].sum(axis=0)
        mtm_array.append(mtm)
         
nifty_intraday(75,500,60)

mtm_array=pd.DataFrame(mtm_array)
date_date_df=pd.DataFrame(date_date)

backtest_df=pd.concat([date_date_df,mtm_array], axis=1)
backtest_df.columns=['date','daily_mtm_per_lot']
backtest_df=backtest_df.dropna()

backtest_df =backtest_df.reset_index(drop=True)
# backtest_df.set_index(['date'], inplace=True)
backtest_df =backtest_df.dropna()

backtest_df['portfolio']=0

for i in range(len(backtest_df)):

    if i==0:
        backtest_df['portfolio'].iloc[i]=1_00_000
    else:
        backtest_df['portfolio'].iloc[i]=backtest_df['portfolio'].iloc[i-1] + backtest_df['daily_mtm_per_lot'].iloc[i]

backtest_df.to_csv(r"C:\Users\DeepakShenoy\Desktop\Quantitative Research\Equity_Strategy_Backtest\backtest_df_nifty_195min.csv")

# cagr=(((backtest_df['portfolio'].iloc[-1]/(backtest_df['portfolio'].iloc[0]))**(1/10))-1)*100

max_return=backtest_df['daily_mtm_per_lot'].max()
min_return=backtest_df['daily_mtm_per_lot'].min()

backtest_df['result'] =np.where( backtest_df['daily_mtm_per_lot'] > 0, 1 ,-1)

positive_condition=backtest_df['result'] ==1
absolute_return_positive = backtest_df[positive_condition]
avg_positive=absolute_return_positive['daily_mtm_per_lot'].mean()
win_rate=absolute_return_positive['result'].sum(axis=0)/(len(backtest_df))
win_rate=win_rate*100

negative_condition=backtest_df['result'] == -1
absolute_return_negative = backtest_df[negative_condition]
avg_negative=absolute_return_negative['daily_mtm_per_lot'].mean()
loss_rate= absolute_return_negative['result'].sum(axis=0)*(-1)/(len(backtest_df))
loss_rate=loss_rate*100

window = 252
Roll_Max_portfolio = backtest_df['portfolio'].rolling(window, min_periods=1).max()
Daily_Drawdown_portfolio = (backtest_df['portfolio']/Roll_Max_portfolio - 1)*100

plt.plot(backtest_df['portfolio'])
plt.title("Equiy_Curve")
plt.show()

plt.plot(Daily_Drawdown_portfolio, color="blue", label="PORTFOLIO")
plt.title("DRAWDOWN")
plt.legend()
plt.show()

print(f"max_return is {max_return} ")
print(f"min_return is {min_return}")
print(f"No of positive days is { absolute_return_positive['result'].sum(axis=0)}")
print(f"No of Negative days is { absolute_return_negative['result'].sum(axis=0)*(-1)}")
# print(f"CAGR is {cagr}")
print(f"Max Drawdown is  {Daily_Drawdown_portfolio.min()}")
print(f"Avg Positive return is {avg_positive}")
print(f"Avg Negative return is {avg_negative}")
print(f"Win rate is {win_rate}")
print(f"Loss rate is {loss_rate}")


