import asyncio
import os
from datetime import datetime, timedelta
import Actions_class
import AccessToken
import sys
import requests
import pandas as pd

today_date = datetime.now().date()

def ohlc_NSE(ISINCODE):
    """Fetches OHLC data from NSE"""
    url = f'https://api.upstox.com/v2/historical-candle/intraday/NSE_EQ%7C{ISINCODE}/1minute'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['data']['candles']
    return None

async def ohlc_lastdayclose(ISINCODE):
    """Fetches OHLC data from NSE"""
    url = f'https://api.upstox.com/v2/historical-candle/NSE_EQ%7C{ISINCODE}/day/{today_date-timedelta(days = 1)}/{today_date-timedelta(days = 2)}'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            yesterday_candle = data['data']['candles']
            return yesterday_candle[0][4]

    return None

async def get_price(isin_code, key):
    """Gets the last price of the stock"""
    isin_code_output = await Actions_class.APIActions.get_quote("NSE_EQ|" + isin_code, key)
    isin_lastprice = isin_code_output['data']
    first_key = list(isin_lastprice.keys())[0]
    return isin_lastprice[first_key]['last_price']

async def wait_until(target_time):
    while datetime.now() < target_time:
        time_remaining = target_time - datetime.now()
        if time_remaining > timedelta(seconds=10):
            await asyncio.sleep(5)
        print(f"Time remaining: {time_remaining}")

async def amount_available(key,percentage):
    cash_avail = await Actions_class.APIActions.get_funds(key)
    if cash_avail['status'] == 'success':
        exact_cash_available = cash_avail['data']['equity']['available_margin']
    else:
        print("Error fetching available funds")
        return
    
    amount_can_be_used = exact_cash_available * (percentage/100)
    print(f"Amount that can be used: {amount_can_be_used}")
    return amount_can_be_used

async def check_market_trend(isin_code,key):
    is_bull = False
    open_price = await get_price(isin_code, key)
    await asyncio.sleep(900)
    close_price = await get_price(isin_code, key)
    print(close_price)
    if abs((close_price - open_price)/close_price)>2:
        sys.exit()

    if close_price>open_price:
        is_bull = True

    return is_bull

async def get_target(is_bull,close_price,percentage):
    if is_bull:
        target = close_price + ((percentage/100)*close_price)
    else:
        target = close_price - ((percentage/100)*close_price)
    return target

async def calculate_buy_sell_ratio(isin_code,key):
    market_quote = await Actions_class.APIActions.get_quote("NSE_EQ|" + isin_code, key)
    data = market_quote['data']
    for symbol, details in data.items():
        total_buy_quantity = details['total_buy_quantity']
        total_sell_quantity = details['total_sell_quantity']

        if total_sell_quantity == 0:
            ratio = float('inf')
        else:
            ratio = total_buy_quantity / total_sell_quantity
    return ratio

async def netchange(isin_code,key):
    market_quote = await Actions_class.APIActions.get_quote("NSE_EQ|" + isin_code, key)
    data = market_quote['data']
    for symbol, details in data.items():
        netchange = details['net_change']  
        return netchange

async def change_per(isin_code,key):
    netchange_data = await netchange(isin_code,key)
    lastday_price = await ohlc_lastdayclose(isin_code)
    return ((netchange_data/lastday_price)*100)

async def check_access(file_path):
    if os.path.exists(file_path):
        modification_time = os.path.getmtime(file_path)
        modification_date = datetime.fromtimestamp(modification_time).date()
        if modification_date != today_date:
            print("Access token is not created today")
            await AccessToken.main()
    else:
        print("Access token is not present in the required location")
        await AccessToken.main()