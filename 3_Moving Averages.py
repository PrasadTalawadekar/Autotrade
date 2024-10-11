import asyncio
import os
from datetime import datetime, timedelta, time
import time
import sys
import requests
import pandas as pd
import Methods as md
import matplotlib.pyplot as plt

# Function to handle asynchronous call for last30days1mins and combine the data
async def fetch_and_combine():
    while True:
        print("yes")
        abc2 = await md.fetch_and_combine('INE256A01028')
        abc2['50 SMA'] = abc2['Close'].rolling(window=50).mean()
        abc2['200 SMA'] = abc2['Close'].rolling(window=200).mean()

        # Get current data (latest row)
        current_df = abc2.tail(1)
        
        current_price = current_df['Close'].values[0]
        current_50_SMA = current_df['50 SMA'].values[0]
        current_200_SMA = current_df['200 SMA'].values[0]

        # Track flags for whether trade is triggered
        sell_flag_50_SMA = False
        buy_flag_50_SMA = False
        sell_flag_200_SMA = False
        buy_flag_200_SMA = False

        # Check for SMA crossings
        if current_50_SMA < current_200_SMA:
            # 50 SMA is below 200 SMA
            if current_price > current_200_SMA:
                # Current price crossed above 200 SMA, set sell target at 50 SMA
                sell_flag_200_SMA = True
                print(f"Sell flag triggered (200 SMA). Target: 50 SMA.")
                
            if current_price < current_50_SMA:
                # Current price crossed below 50 SMA, set buy target at 200 SMA
                buy_flag_50_SMA = True
                print(f"Buy flag triggered (50 SMA). Target: 200 SMA.")
                
        else:
            # 50 SMA is above 200 SMA
            if current_price > current_50_SMA:
                # Current price crossed above 50 SMA, set sell target at 200 SMA
                sell_flag_50_SMA = True
                print(f"Sell flag triggered (50 SMA). Target: 200 SMA.")
                
            if current_price < current_200_SMA:
                # Current price crossed below 200 SMA, set buy target at 50 SMA
                buy_flag_200_SMA = True
                print(f"Buy flag triggered (200 SMA). Target: 50 SMA.")

        # Sleep for 5 minutes before next check
        #time.sleep(5 * 60)

        # Track previous prices and SMAs
        older_price = current_price
        older_50_SMA = current_50_SMA
        older_200_SMA = current_200_SMA





        
        print(abc2)

# Running the asynchronous function using asyncio
asyncio.run(fetch_and_combine())
