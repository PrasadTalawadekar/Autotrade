AUTO_TRADE USING UPSTOX API

INDEX:
	Strategies:
1.	0_Download_NiftyFiles
2.	1_Making_Summary
3.	2_BuyerSellerRatio
4.	3_Moving Averages
5.	4_Swing trading prices

Classes
1.	Authorization
2.	Methods

















Authorization

Authorization is the Namespace created which redirects to the class named as APIActions.
APIActions is class which includes all the basic methods we need to perform in the process of automation of trading. As it is purely dependent on API’s we have tried to pull all the API methods under the Namespace Authorization.

Methods()
1.	get_website: returning to the desired authorization website
2.	final_output: returning to the API key.
3.	get_funds: Returning the funds and margin available
4.	get_holdings: Return the holdings available in our trading account
5.	get_short_holdings: Return short term holdings
6.	get_brokerage: Return Brokerage for the specific transaction
7.	get_quote: Return the current quote of IN number of the script
8.	todays_trade: Return the trades of the day
9.	buy_delivery_market: Action to buy delivery for a script on market rate
10.	buy_Intraday_market: Action to buy script as a Intraday on market rate
11.	sell_delivery_market: Action to sell delivery for a script on market rate
12.	sell_Intraday_market: Action to sell script as Intraday on market rate
13.	create_folder: creating a folder in laptop
14.	convert_json: convert data in Json
15.	encode_symbol: encoding of data
16.	GetCandles: Get the candles of specific symbol for specific time range


Methods
Methods Namespace is created to save all the methods which are being used for all strategies.

Methods()
1.	ohlc_NSE: Returns candles list of intraday for one minute
2.	ohlc_lastdayclose: Last Trading Day candle
3.	get_price: Get last trading price
4.	wait_until: Code execution time 
5.	amount_available: Fetch the margin available
6.	check_market_trend: 15 mins wait and understand if it is increased or decreased
7.	get_target: To get the target value of script
8.	calculate_buy_sell_ratio: Get the ration of (no of buyers/ no of sellers)
9.	netchange: get the net change in the script
10.	change_per: change percentage
11.	check_access: Check the access and make update the access key if required.
Strategies:
0_Download_NiftyFiles
	Get to the chrome driver and download all the desired nifty files which will help us to execute strategies on corresponding share present in that index.
1_Making_Summary
	Using the ‘ind_niftytotalmarket_list.csv’ we will create a df which will consider and check all the possible indexes and mark them as true and false in corresponding category.
2_BuyerSellerRatio
	This will go in corresponding index and check for the buyer : seller ratio and if the ratio is 1:2 or 2:1. If the net change is not dramatically high. This will execute buy or sell intraday.
3_Moving Averages
	Moving averages give us 50SMA and 200SMA ka data which gives this dataframe which help us to decide our trade
4_Swing trading prices
	This helps us to process the ‘ind_niftytotalmarket_list.csv’ with 52 week high and 52 week low which help us to buy the scripts which lies near 52 week low but are in better indexes



Credits: Book | Intraday Trading Strategies (Part-I) | Abhijit Zingade
