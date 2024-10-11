import asyncio
import os
from datetime import datetime, timedelta , time
import Authorization
import sys
import requests
import pandas as pd
import Methods as md

current_dir = r'C:\Users\Prasad\Music\Share market'
file_path = os.path.join(current_dir, 'access_token.txt')
############################################################################################
#Time declaration
today_date = datetime.now().date()

time_9_10 = time(hour=9, minute=10)  
begin_time = datetime.combine(today_date, time_9_10)

time_9_15 = time(hour=9, minute=15) 
Market_time = datetime.combine(today_date, time_9_15)

time_9_20 = time(hour=9, minute=20) 
execution_time = datetime.combine(today_date, time_9_20)

time_14_20 = time(hour=14, minute=30) 
cutoff_time = datetime.combine(today_date, time_14_20)


############################################################################################



async def main():
    await md.check_access(file_path)
    await md.wait_until(begin_time)
    with open(file_path, 'r') as file:
        key = file.read().strip()

    path = r'C:\Users\Prasad\Music\Share market\NiftyDataBase\Nifty exports\ind_nifty50list.csv'
    df = pd.read_csv(path)
    dict = {}
    isin_arr = []

    for isin_code in df['ISIN Code']:     # make dictionary post settling buyer,seller ratio and net
        print(isin_code)        
        buy_sell = await md.calculate_buy_sell_ratio(isin_code,key)   #Buy/Sell
        print(buy_sell)
        net = await md.netchange(isin_code,key)   #Net change from yesterday close
        if buy_sell > 2 or buy_sell < 0.5:
            if net > -1 and net < 1 :
                dict[isin_code] = [buy_sell,net]
                isin_arr.append(isin_code)
                
    await md.wait_until(Market_time)

    isin_order = []
    order_dict = {}

    for isin_code in isin_arr:           # Buyer seller ratio continues order_dict and isin_orders filtered
        buy_sell = await md.calculate_buy_sell_ratio(isin_code,key)
        net = await md.netchange(isin_code,key)

        if dict[isin_code][0]<0.5:
            if buy_sell < 0.5:
                order_dict[isin_code] = 'Sell'
                isin_order.append(isin_code)
        else:
            if buy_sell > 2:
                order_dict[isin_code] = 'Buy'
                isin_order.append(isin_code)

    amount_can_be_used = await md.amount_available(key,10)
    await md.wait_until(execution_time)
    execution_dict={}

    for isin in isin_order:
        close_price = await md.get_price(isin_code, key)
        execution_dict[isin] = [close_price, order_dict[isin]]


        if order_dict[isin] == 'Buy':
            close_price = await md.get_price(isin_code, key)
            quantity = int(amount_can_be_used / close_price)
            await Authorization.APIActions.buy_Intraday_market(quantity, "NSE_EQ|" + isin_code, key)

        if order_dict[isin] == 'Sell':
            close_price = await md.get_price(isin_code, key)
            quantity = int(amount_can_be_used / close_price)
            await Authorization.APIActions.sell_Intraday_market(quantity, "NSE_EQ|" + isin_code, key)
    


if __name__ == "__main__":
    asyncio.run(main())