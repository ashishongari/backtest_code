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
import datetime 
from datetime import datetime, timedelta


def sharpe_ratio(day):
    
    """
    Day is a variable which is used to defimne a rolling sharpe ratio, I.E day=30, Moving sharpe ratio of 30 days
    """
    
    ##############################################################################################################################################

    """
    Define a universe of stock, calculate moving sharpe ratio, get the data from repo, it is names as stock_data_eod.csv
    """
    df=pd.read_csv(r"", index_col=0)

    df_pct=df.pct_change()
    df_pct_sum=df_pct.rolling(window=day).sum()
    df_std=df_pct.rolling(window=day).std()
    df_sharpe_ratio=df_pct_sum.div(df_std)
    date_set=df_sharpe_ratio.index
    # print(df_sharpe_ratio)

    date_set=date_set[day:]
    date_set_df=pd.DataFrame(date_set)
    date_set_df.columns=['date']

    date_set_df['trading_day']=0
    # date_set_df=date_set_df.reset_index(drop=True)

########################################################################################################################################################

    """
    Define Buy and exit trading day for system
    """
    for i in range(len(date_set_df)):
        
        if i%25 ==0:
            date_set_df['trading_day'].iloc[i]=date_set_df['date'].iloc[i]
           
        else:
            date_set_df['trading_day'].iloc[i]=0
            

    condition=date_set_df['trading_day'] !=0
    date_set_df=date_set_df[condition]

    # trading_day=date_set_df['trading_day']
    # trading_day=np.array(trading_day)
    # new_df_sharpe_ratio=df_sharpe_ratio.copy()


    #####################################################################################################################################################

    """
    Define top 15 stocks which have highest sharpe ratio on each trading and rebalance every 15 days according to top 15 rank
    """
    #STOCK_LIST

    stock_list=[]
    trading_day=date_set_df['trading_day']
    trading_day=np.array(trading_day)
    new_df_sharpe_ratio=df_sharpe_ratio.copy()
    # print(new_df_sharpe_ratio)


    for i in range(len(trading_day)):

        new_df_sharpe_ratio=new_df_sharpe_ratio.copy()

        live_sharpe_ratio=new_df_sharpe_ratio.loc[trading_day[i]]
        live_sharpe_ratio=pd.DataFrame(live_sharpe_ratio)
        live_sharpe_ratio.columns=['sharpe_ratio']
        live_sharpe_ratio=live_sharpe_ratio.dropna()
        new =live_sharpe_ratio.sort_values(by='sharpe_ratio', ascending=False)
        
        list_stock=new[:14]
       
        new_df=df.copy()
        new_df=df.loc[trading_day[i]]
        new_df=pd.DataFrame(new_df)
        new_df.columns=['price']

        backtest_df=pd.concat([list_stock,new_df], axis=1)
        backtest_df=backtest_df[:15]
        stock_list.append(backtest_df.index)

        
    stock_list=pd.DataFrame(stock_list)
    trading_day=pd.DataFrame(trading_day)

    buy_list_df=pd.concat([trading_day, stock_list], axis=1)
    buy_list_df.columns=['date','stock_1','stock_2','stock_3','stock_4','stock_5','stock_6','stock_7','stock_8','stock_9','stock_10','stock_11','stock_12','stock_13','stock_14','stock_15']
    print(buy_list_df)

#####################################################################################################################################################################

    """
    Calcaulte the entry price of list of stocks selected by system

    """
    #ENTRY_PRICE_LIST

    price_list_buy=[]
    trading_day=date_set_df['trading_day']
    trading_day=np.array(trading_day)
    new_df_sharpe_ratio=df_sharpe_ratio.copy()

    for i in range(len(trading_day)):

        live_sharpe_ratio=new_df_sharpe_ratio.loc[trading_day[i]]
        live_sharpe_ratio=pd.DataFrame(live_sharpe_ratio)
        live_sharpe_ratio.columns=['sharpe_ratio']
        new =live_sharpe_ratio.sort_values(by='sharpe_ratio', ascending=False)
        list_stock=new[:14]

        new_df=df.copy()
        new_df=df.loc[trading_day[i]]
        new_df=pd.DataFrame(new_df)
        new_df.columns=['price']

        backtest_df=pd.concat([list_stock,new_df], axis=1)
        backtest_df=backtest_df[:15]
        
        backtest_df=backtest_df.reset_index(drop=True)

        price_list_buy.append(backtest_df['price'])
        
    price_list_buy=pd.DataFrame(price_list_buy)
    price_list_buy=price_list_buy.reset_index(drop=True)
    trading_day=pd.DataFrame(trading_day)
    price_list_df_entry=pd.concat([trading_day, price_list_buy], axis=1)
    price_list_df_entry.columns=['date','stock_1','stock_2','stock_3','stock_4','stock_5','stock_6','stock_7','stock_8','stock_9','stock_10','stock_11','stock_12','stock_13','stock_14','stock_15']
    price_list_df_entry=price_list_df_entry.iloc[:-1]

    print(price_list_df_entry)

##############################################################################################################################################################################
    """
    Calculate the exit price of stocks as per generated by systmem
    """
    #EXIT_PRICE_LIST

    price_list_exit=[]
    trading_day=date_set_df['trading_day']
    trading_day=np.array(trading_day)
    # trading_day=trading_day[1:len(trading_day)]
    # trading_day=trading_day[1:-1]

    for i in range(len(trading_day)-1):

        exit_list_df=buy_list_df.copy()
        exit_list_df=exit_list_df.set_index('date')
        exit_list_stock_df=exit_list_df.loc[trading_day[i]]
        exit_list_stock_df=np.array(exit_list_stock_df)
        
        exit_list_stock_df=pd.DataFrame(exit_list_stock_df)
        exit_list_stock_df.columns=['stock']
        exit_list_stock_df['date']=trading_day[i+1]
        
        exit_list_stock_df=exit_list_stock_df.set_index('stock')

        exit_price=df.copy()
        exit_price=exit_price.loc[trading_day[i+1]]
        
        backtest_df=pd.concat([exit_list_stock_df,exit_price], axis=1)
        backtest_df=backtest_df.dropna()
        backtest_df.columns=['date','price']
        backtest_df=backtest_df['price']
        backtest_df=backtest_df.reset_index(drop=True)

        price_list_exit.append(backtest_df)


    price_list_exit=pd.DataFrame(price_list_exit)
    price_list_exit=price_list_exit.reset_index(drop=True)
    trading_day=pd.DataFrame(trading_day)
    price_list_df_exit=pd.concat([trading_day, price_list_exit], axis=1)
    price_list_df_exit.columns=['date','stock_1','stock_2','stock_3','stock_4','stock_5','stock_6','stock_7','stock_8','stock_9','stock_10','stock_11','stock_12','stock_13','stock_14','stock_15']
    price_list_df_exit['date']=price_list_df_exit['date'].shift(-1)
    price_list_df_exit=price_list_df_exit.iloc[:-1]
    print(price_list_df_exit)

# ##################################################################################################################################################################################
    """
    Calculate the month on month return generated by system
    """

    entry_price=price_list_df_entry.copy()
    entry_price=entry_price.drop('date', axis='columns')
    # print(entry_price)

    exit_price=price_list_df_exit.copy()
    exit_price=exit_price.drop('date', axis='columns')
    # print(exit_price)
    
    diff_df=exit_price.sub(entry_price)
    diff_pct=diff_df.div(entry_price)
    diff_pct=diff_pct*(100/15)

    absolute_return=diff_pct.sum(axis=1)
    absolute_return=pd.DataFrame(absolute_return)
    absolute_return.columns=['absolute_return']
    absolute_return['absolute_return']=absolute_return['absolute_return'].shift(1)
    trading_day=np.array(trading_day)
    trading_day=pd.DataFrame(trading_day)
    absolute_return['date']=trading_day
    print(absolute_return)

  
    return 

sharpe_ratio(30)
