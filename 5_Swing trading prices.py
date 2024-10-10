import pandas as pd
import requests
from datetime import date
from dateutil.relativedelta import relativedelta  

# Get today's date and one year ago
today_day = date.today()
print(f"Today's date: {today_day}")

one_year_ago = today_day - relativedelta(years=1)
print(f"One year ago: {one_year_ago}")

def HighLow(ISINCODE):
    url = f'https://api.upstox.com/v2/historical-candle/NSE_EQ%7C{ISINCODE}/month/{today_day}/{one_year_ago}'
    url_2 = f'https://api.upstox.com/v2/historical-candle/NSE_EQ%7C{ISINCODE}/day/{today_day}'
    headers = {'Accept': 'application/json'}
    
    try:
        # Fetch historical data
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        
        # Fetch current price
        response_2 = requests.get(url_2, headers=headers)
        response_2.raise_for_status()  
        
        current_price_data = response_2.json()
        historical_data = response.json()
        
        if current_price_data['status'] == 'success':
            candles = current_price_data['data']['candles']
            if candles:
                cur_price = candles[0][4]
            else:
                cur_price = None
        else:
            cur_price = None
        
        if historical_data['status'] == 'success':
            candles = historical_data['data']['candles']
            High = float('-inf')
            Low = float('inf')
            if candles:
                for a in candles:
                    if a[2] > High:
                        High = a[2]
                    if a[3] < Low:
                        Low = a[3]
                return [High, Low, cur_price]
            
            else:
                return [None, None, cur_price]
        else:
            return [None, None, cur_price]
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return [None, None, None]

# Load the CSV file
csv_required = "C:\\Users\\Prasad\\Music\\Share market\\Finding script\\summary.csv"
df = pd.read_csv(csv_required)

# Create new columns for High, Low, and Current price
df['High'] = None
df['Low'] = None
df['Current price'] = None

# Update the DataFrame with High, Low, and Current price values
for index, row in df.iterrows():
    isin_code = row['ISIN Code']
    high_low_values = HighLow(isin_code)
    print(isin_code)
    if high_low_values:
        df.at[index, 'High'] = high_low_values[0]
        df.at[index, 'Low'] = high_low_values[1]
        df.at[index, 'Current price'] = high_low_values[2]
        print(high_low_values)

# Save the updated DataFrame to the CSV
df.to_csv(csv_required, index=False)
