import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import datetime
from datetime import date

import requests
import urllib.parse


'''
# Welcome to our stock prediction model.

On the following page we'll make you rich. You are welcome!
'''

options_8000 = pd.read_csv('nasdaq_current_list_12112012.csv')
options = list(options_8000['Name'])
options.insert(0, '')

stock = st.selectbox("Start typing a stock name", options)


'''
#### You requested prediction for the following stock: 
'''

st.write(stock)


'''
### Here is some fake data to use for testing (with date display relative to today): 
'''

# get price prediction from UI
url = "http://127.0.0.1:8000/predict"
params = {'stock' : stock
            }
response = requests.get(url, params = params)

stock_prediction = response.json() 

# create sample input data (predictions for the next 7 days)
def get_fake_data():
    data = {'Day1': [3.2],
            'Day2': [3.4],
            'Day3': [2.8], 
            'Day4': [3.9], 
            'Day5': [4.6], 
            'Day6': [3.1], 
            'Day7': [5.2]
            }

    df = pd.DataFrame(data).T
    df.rename(columns={0: 'stock_price'}, inplace=True)

    # add column with date (relative to 'today')
    today = date.today()
    tomorrow = today + datetime.timedelta(days = 1)
    Day3 = f'{today + datetime.timedelta(days = 2)}'
    Day4 = f'{today + datetime.timedelta(days = 3)}'
    Day5 = f'{today + datetime.timedelta(days = 4)}'
    Day6 = f'{today + datetime.timedelta(days = 5)}'
    Day7 = f'{today + datetime.timedelta(days = 6)}'

    dates = ['today', 'tomorrow', Day3, Day4, Day5, Day6, Day7]

    # add dates as new column to the df
    df['date'] = dates
    
    
    return df


stock_prediction_fake = get_fake_data()

st.write(stock_prediction_fake)


'''

### Visualise predictions

'''


fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(stock_prediction_fake['date'], stock_prediction_fake['stock_price'])
ax.scatter(stock_prediction_fake['date'], stock_prediction_fake['stock_price'])
# plt.style.use('fast')
st.pyplot(fig)

