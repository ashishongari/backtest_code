import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import pandas_datareader as pdr
import yfinance as yf
from datetime import date
import calendar
import datetime as dt

"""
Go Long on Nifty if Friday's 3.15 PM  Close > 9.16 AM Open else Short and exit on Monday 9.16 AM Close

"""

def nifty_open(lot_size):
    
    data_1=pd.read_csv(r"",parse_dates=True, index_col=0)
    
    date_data=data_1['Date'].unique()
    date_df=pd.DataFrame(date_data)
    date_df.columns=['Date']

    date_df['weekday_name']=0

    for i in range(len(date_df)):
        
        born = datetime.datetime.strptime(date_df['Date'].iloc[i], '%d-%m-%Y').weekday() 
        date_df['weekday_name'].iloc[i]=calendar.day_name[born]

    
    date_df['Trading_day']=0
    date_df['Next_day']=0

    for i in range(len(date_df)-1):

        if date_df['weekday_name'].iloc[i]=='Friday':

            date_df['Trading_day'].iloc[i] = date_df['Date'].iloc[i]
            date_df['Next_day'].iloc[i] = date_df['Date'].iloc[i+1]
        else:
            date_df['Trading_day'].iloc[i] = 0
            date_df['Next_day'].iloc[i] = 0
        
    condition=date_df['Trading_day'] != 0
    date_df=date_df[condition]

    date_df=date_df[['Trading_day','Next_day']]
    date_df=date_df.reset_index(drop=True)

    date_df['trading_day_open']=0
    date_df['trading_day_close']=0
    date_df['next_day_open']=0

    for i in range(len(date_df)):
        
        live_data_trading_data=data_1.loc[data_1['Date']==date_df['Trading_day'][i]]
        live_data_next_data=data_1.loc[data_1['Date']==date_df['Next_day'][i]]
        print(live_data_trading_data)

        trading_day_open =live_data_trading_data['Open'][1]
        trading_day_close =live_data_trading_data['Close'][-15]

        next_day_open=live_data_next_data['Close'][1]

        date_df['trading_day_open'].iloc[i]=trading_day_open
        date_df['trading_day_close'].iloc[i]=trading_day_close
        date_df['next_day_open'].iloc[i]=next_day_open


    date_df['Short_Long'] =np.where( date_df['trading_day_close'] >  date_df['trading_day_open'], 1, -1)

    date_df['MTM']=0

    for i in  range(len(date_df)):

        if date_df['Short_Long'].iloc[i]==1:

            date_df['MTM'].iloc[i] = (date_df['next_day_open'].iloc[i] - date_df['trading_day_close'].iloc[i])*lot_size

        elif date_df['Short_Long'].iloc[i]== -1:

            date_df['MTM'].iloc[i] = ((date_df['next_day_open'].iloc[i] - date_df['trading_day_close'].iloc[i])*lot_size)*(-1)

        else:
            date_df['MTM'].iloc[i]=0

    print(f"MTM of strategy is {date_df['MTM'].sum()}")
    
    return
    
nifty_open(75)

############################################################################################################################################


"""
Go Long on Nifty if Friday's 3.15 PM  Close > 9.16 AM Open else Short and exit on Monday 3.15 PM Close

"""
def nifty_close(lot_size):
    
    data_1=pd.read_csv(r"",parse_dates=True, index_col=0)
    
    date_data=data_1['Date'].unique()
    date_df=pd.DataFrame(date_data)
    date_df.columns=['Date']

    date_df['weekday_name']=0

    for i in range(len(date_df)):
        
        born = datetime.datetime.strptime(date_df['Date'].iloc[i], '%d-%m-%Y').weekday() 
        date_df['weekday_name'].iloc[i]=calendar.day_name[born]

    date_df['Trading_day']=0
    date_df['Next_day']=0

    for i in range(len(date_df)):

        if date_df['weekday_name'].iloc[i]=='Friday':

            date_df['Trading_day'].iloc[i] = date_df['Date'].iloc[i]
            date_df['Next_day'].iloc[i] = date_df['Date'].iloc[i+1]
        else:
            date_df['Trading_day'].iloc[i] = 0
            date_df['Next_day'].iloc[i] = 0
        
    condition=date_df['Trading_day'] != 0
    date_df=date_df[condition]

    date_df=date_df[['Trading_day','Next_day']]
    date_df=date_df.reset_index(drop=True)

    date_df['trading_day_open']=0
    date_df['trading_day_close']=0
    date_df['next_day_open']=0

    for i in range(len(date_df)):
        
        live_data_trading_data=data_1.loc[data_1['Date']==date_df['Trading_day'][i]]
        live_data_next_data=data_1.loc[data_1['Date']==date_df['Next_day'][i]]
        print(live_data_trading_data)

        trading_day_open =live_data_trading_data['Open'][1]
        trading_day_close =live_data_trading_data['Close'][-15]

        next_day_open=live_data_next_data['Close'][-15]

        date_df['trading_day_open'].iloc[i]=trading_day_open
        date_df['trading_day_close'].iloc[i]=trading_day_close
        date_df['next_day_open'].iloc[i]=next_day_open

    date_df['Short_Long'] =np.where( date_df['trading_day_close'] >  date_df['trading_day_open'], 1, -1)
    date_df['MTM']=0


    for i in  range(len(date_df)):

        if date_df['Short_Long'].iloc[i]==1:

            date_df['MTM'].iloc[i] = (date_df['next_day_open'].iloc[i] - date_df['trading_day_close'].iloc[i])*lot_size

        elif date_df['Short_Long'].iloc[i]== -1:

            date_df['MTM'].iloc[i] = ((date_df['next_day_open'].iloc[i] - date_df['trading_day_close'].iloc[i])*lot_size)*(-1)

        else:
            date_df['MTM'].iloc[i]=0


    print(f"MTM of strategy is {date_df['MTM'].sum()}")

    return 

nifty_close(75)


