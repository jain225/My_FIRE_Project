import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
import csv
import sqlite3
import time
import datetime
import random
import json
import requests
from datetime import datetime 
from datetime import date


### CONNECTING TO DATABASE ###
conn = sqlite3.connect('stockmarket.db')
c = conn.cursor()




### CREATING DATAFRAME WITH STOCK TICKERS ###
    ### OPTION 1 - IMPORTING WITH CSV ###
def stock_csv():
    #stock_csv_file = pd.read_csv (r'C:\Users\home\Desktop\code_projects\db\alpha_vantage_active_stocks.csv')
    #stock_csv_file = pd.read_csv (r'C:\Users\home\Desktop\code_projects\db\alpha_vantage_active_stocks2.csv')
    stock_csv_file = pd.read_csv (r'C:\Users\home\Desktop\code_projects\db\alpha_vantage_active_stocks3.csv')

    df = pd.DataFrame(stock_csv_file)
    df = df.rename(columns = {"symbol":"stock_ticker", "name":"stock_name", "exchange":"stock_exchange", "ipoDate":"stock_ipoDate", "delistingDate":"stock_delistingDate", "status":"stock_status"})

    stock_updateTime = date.today()
        # append this to the dataframe 

    update_table_stocks = """
        INSERT INTO stocks (stock_ticker,
                            stock_name,
                            stock_exchange,
                            stock_ipoDate,
                            stock_delistingDate,
                            stock_status,
                            stock_updateTime
                            )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (stock_ticker) DO UPDATE SET 
                stock_name = EXCLUDED.stock_name,
                stock_exchange = EXCLUDED.stock_exchange,
                stock_ipoDate = EXCLUDED.stock_ipoDate,
                stock_delistingDate = EXCLUDED.stock_delistingDate,
                stock_status = EXCLUDED.stock_status,
                stock_updateTIme = EXCLUDED.stock_updateTime
            """

    for i in range(len(df)):
        values = tuple(df.iloc[i])
        c.execute(update_table_stocks, values)
        conn.commit()





    ### OPTION 2 - IMPORTING FROM ALPHA VANTAGE ###
        # https://www.alphavantage.co/documentation/
            # Fundamental Data > Listing And Delisting Status
            # https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo
def stock_api():
    base_url = 'https://www.alphavantage.co/query?'
    params = {'function': 'LISTING_STATUS',
            'apikey': 'S1CBJQPC92YX01S8'}
    response_data_overview = requests.get(base_url, params=params)
    
    # create dataframe from json or something
    
    # append current date and time stamp to dataframe
    stock_updateTime = date.today()

    update_table_stocks = """
        INSERT INTO stocks (stock_ticker,
                            stock_name,
                            stock_exchange,
                            stock_ipoDate,
                            stock_delistingDate,
                            stock_status,
                            stock_updateTime
                            )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (stock_ticker) DO UPDATE SET 
                stock_name = EXCLUDED.stock_name,
                stock_exchange = EXCLUDED.stock_exchange,
                stock_ipoDate = EXCLUDED.stock_ipoDate,
                stock_delistingDate = EXCLUDED.stock_delistingDate,
                stock_status = EXCLUDED.stock_status,
                stock_updateTIme = EXCLUDED.stock_updateTime
            """

    for i in range(len(df)):
        values = tuple(df.iloc[i])
        c.execute(update_table_stocks, values)
        conn.commit()




### UPDATING DATABASE ###
    # We can choose which option to use to update the database
stock_csv()
#stock_api()



c.close()
conn.close()