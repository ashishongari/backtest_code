# Importing libraries
import pandas as pd  
import numpy as np  
from matplotlib.ticker import NullFormatter
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
%matplotlib inline
import pandas_datareader as pdr
import datetime 
import yfinance as yf
from sklearn import linear_model
import seaborn as sns
from nsepy import get_history
from datetime import date
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
