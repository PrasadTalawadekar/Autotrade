import os
import requests
import json
from typing import List, Dict
import aiohttp
from urllib.parse import quote
import urllib

class APIActions:
    api_key = "API KEY here"
    api_secret = "API Sercret here"
    redirect_uri = "Redirect URI here"
    state = "Statr here"
    authorization_code = None

    @staticmethod
    def get_website() -> str:
        auth_url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={APIActions.api_key}&redirect_uri={APIActions.redirect_uri}&state={APIActions.state}"
        return auth_url

    @staticmethod
    async def final_output(authorization_code: str) -> str:
        token_url = "https://api.upstox.com/v2/login/authorization/token"
        payload = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "client_id": APIActions.api_key,
            "client_secret": APIActions.api_secret,
            "redirect_uri": APIActions.redirect_uri
        }

        try:
            response = requests.post(token_url, data=payload)
            if response.status_code == 200:
                access_token = response.json()["access_token"]
                return access_token
            else:
                return "Something Failed"
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            return "Something Failed"

    @staticmethod
    async def get_funds(your_access_token: str) -> str:
        url = "https://api.upstox.com/v2/user/get-funds-and-margin"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return (response.text)
        else:
            return (f"Failed to retrieve data. Status Code: {response.status_code}")

    @staticmethod
    async def get_holdings(your_access_token: str) -> str:
        url = "https://api.upstox.com/v2/portfolio/long-term-holdings"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve data. Status Code: {response.status_code}"

    @staticmethod
    async def get_short_holdings(your_access_token: str) -> str:
        url = "https://api.upstox.com/v2/portfolio/short-term-positions"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return (json.dumps(data, indent=4))
                else:
                    return (f"Failed to retrieve data. Status Code: {response.status}")

    @staticmethod
    async def get_brokerage(instrument_token, quantity, product, transaction_type, price, your_access_token)-> str:
        url = "https://api.upstox.com/v2/charges/brokerage"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }
        params = {
            "instrument_token": instrument_token,   #NSE_EQ|INE848E01016
            "quantity": str(quantity),
            "product": product,
            "transaction_type": transaction_type,
            "price": str(price)
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return(json.dumps(data, indent=4))
                else:
                    return(f"Failed to retrieve data. Status Code: {response.status}")

    @staticmethod
    async def get_quote(instrument_token, your_access_token):
            url = "https://api.upstox.com/v2/market-quote/quotes"
            code = your_access_token
            encoded_instrument_token = APIActions.encode_symbol(instrument_token)

            queryParams = {
                "instrument_key": encoded_instrument_token
            }

            # Construct query string
            queryString = "&".join([f"{key}={value}" for key, value in queryParams.items()])
            requestUrl = f"{url}?{queryString}"

            headers = {
                "Accept": "application/json",
                "Authorization": "Bearer " + code
            }

            try:
                # Send GET request
                response = requests.get(requestUrl, headers=headers)
                if response.status_code == 200:
                    responseData = response.json()
                    return responseData
                else:
                    return f"Failed to retrieve data. Status Code: {response.status_code}"
            except requests.RequestException as ex:
                # Handle HTTP request exceptions
                print("HTTP Request Exception:", ex)
                return "Failed to retrieve data due to a network error."
            except Exception as ex:
                # Handle other exceptions
                print("Error:", ex)
                return "An error occurred while processing the request."

    @staticmethod
    async def todays_trade(your_access_token):
        url = "https://api.upstox.com/v2/order/trades/get-trades-for-day"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(json.dumps(data, indent=4))
                else:
                    print(f"Failed to retrieve data. Status Code: {response.status}")

    @staticmethod
    async def buy_delivery_market(quantity, instrument_token, your_access_token):
        url = "https://api.upstox.com/v2/order/place"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }
        data = {
            "quantity": quantity,
            "product": "D",
            "validity": "DAY",
            "price": 0,
            "instrument_token": instrument_token,
            "order_type": "MARKET",
            "transaction_type": "BUY",
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "is_amo": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(json.dumps(data, indent=4))
                else:
                    print(f"Failed to place order. Status Code: {response.status}")

    @staticmethod
    async def buy_Intraday_market(quantity, instrument_token, your_access_token):
        url = "https://api.upstox.com/v2/order/place"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }
        data = {
            "quantity": quantity,
            "product": "I",
            "validity": "DAY",
            "price": 0,
            "instrument_token": instrument_token,
            "order_type": "MARKET",
            "transaction_type": "BUY",
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "is_amo": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(json.dumps(data, indent=4))
                else:
                    print(f"Failed to place order. Status Code: {response.status}")

    @staticmethod
    async def sell_delivery_market(quantity, instrument_token, your_access_token):
        url = "https://api.upstox.com/v2/order/place"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }
        data = {
            "quantity": quantity,
            "product": "D",
            "validity": "DAY",
            "price": 0,
            "instrument_token": instrument_token,
            "order_type": "MARKET",
            "transaction_type": "SELL",
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "is_amo": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(json.dumps(data, indent=4))
                else:
                    print(f"Failed to place order. Status Code: {response.status}")

    @staticmethod
    async def sell_Intraday_market(quantity, instrument_token, your_access_token):
        url = "https://api.upstox.com/v2/order/place"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {your_access_token}"
        }
        data = {
            "quantity": quantity,
            "product": "I",
            "validity": "DAY",
            "price": 0,
            "instrument_token": instrument_token,
            "order_type": "MARKET",
            "transaction_type": "SELL",
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "is_amo": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(json.dumps(data, indent=4))
                else:
                    print(f"Failed to place order. Status Code: {response.status}")

    @staticmethod
    async def convert_position(your_access_token):
        url = "https://api.upstox.com/v2/portfolio/convert-position"

        data = {
            "instrument_token": "NSE_EQ|INE699H01024",
            "new_product": "I",
            "old_product": "D",
            "transaction_type": "SELL",
            "quantity": 1
        }

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + your_access_token
        }

        try:
            # Send the PUT request
            response = requests.put(url, json=data, headers=headers)

            # Check the response status code
            if response.status_code == 200:
                # Read the response content
                response_data = response.json()
                print("Response Code:", response.status_code)
                print("Response Body:", response_data)
            else:
                # Handle non-success status code
                error_message = response.text
                print("Failed to convert position. Status Code:", response.status_code)
                print("Error Message:", error_message)
        except requests.RequestException as ex:
            # Handle HTTP request exceptions
            print("HTTP Request Exception:", ex)
        except Exception as ex:
            # Handle other exceptions
            print("Error:", ex)

    @staticmethod
    def create_folder(folder_path: str) -> None:
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print("Folder created successfully.")
            else:
                print("Folder already exists.")
        except Exception as ex:
            print(f"Error creating folder: {str(ex)}")

    @staticmethod
    def convert_json(json_string: str) -> str:
        json_data = json.loads(json_string)
        new_data_list = []

        for item in json_data["data"]:
            new_data = {
                "company_name": item["company_name"],
                "tradingsymbol": item["tradingsymbol"],
                "quantity": item["quantity"],
                "last_price": item["last_price"],
                "average_price": item["average_price"],
                "change": round(-((item["average_price"] - item["last_price"]) * item["quantity"]), 2),
                "instrument_token": item["instrument_token"]
            }
            new_data_list.append(new_data)

        new_json_data = {
            "data": new_data_list
        }

        return json.dumps(new_json_data, indent=4)


    @staticmethod
    def encode_symbol(symbol):
        encoded_symbol = urllib.parse.quote(symbol, safe='')
        return encoded_symbol
    @staticmethod
    async def GetCandles(symbol, timeInterval, startDate, endDate):
        encodedSymbol = APIActions.encode_symbol(symbol)
        url = f"https://api.upstox.com/v2/historical-candle/{encodedSymbol}/{timeInterval}/{endDate}/{startDate}"
        print(url)

        headers = {
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                return "No data"
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "No data"
    