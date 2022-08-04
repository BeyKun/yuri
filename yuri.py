from binance.client import Client
from binance.enums import *
from datetime import datetime
from tabulate import tabulate
from config import *
import json, pandas, os.path, matplotlib as plt

from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import RSIStrategy

"""
@version 0.1

Yuri is a bot for trading Crypto based on Python
the goals of this bot is to make money when we'r sleep and do another things

Feature on Development
- Connect with Binance ✅
- Download Historical Kline Data ✅
- Support RSI, MACD, (Other Indicator Strategy on the future) ✅ 
- Backtesting ✅
- Realtime Websocket Kline
- Automatic Order
- Store Log to DB Postgre
- UI Monitoring with Vue
- Candle Stick Chart
- Future Market
- Multi Market
- Reporting
- Optimiization

"""
class Yuri:

    #initiilize Yuri
    def __init__(self):
        # Connect to Binance
        self.client = Client(API_KEY, API_SECRET)

    # Getting historical data and store to json file
    # if downloaded data not exist then download the data from Binance
    def getDataHistorical(self):
        print("Getting Data...")
        data = []
        if os.path.isfile(PATH_FILE_DOWNLOAD):
            print("Load from existing data..")
            file = open(PATH_FILE_DOWNLOAD)
            data = json.load(file)
        else:
            print("Download Data..")
            data = self.client.get_historical_klines(SYMBOL, TIMEFRAME, "2022-01-01", "2022-08-04")
            with open(f"{PATH_DOWNLOAD_DATA}/{SYMBOL}_{TIMEFRAME}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        return data
    
    # Convert unix timestamp to Datetime
    def toDatetime(self, unixtime):
        return datetime.fromtimestamp(unixtime / 1000)

    # Backtesting using RSI and MACD
    def backtesting(self):
        #getting data historical, store to pandas dataframe and also format those data 
        data = self.getDataHistorical()
        dataframe = pandas.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                                    'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                                                    'taker_buy_quote_asset_volume', 'etc'])
        
        # initialize variable 
        closes = []
        in_position = False
        positions = []
        balance = BASE_BALANCE
        temp_balance = 0
        coins = 0
        total_trades = 0
        total_win = 0
        total_lose = 0


        #Aniliyzing the market with the close price only and checking the signal with RSI and MACD
        print("Anlyzing...")
        for i, row in dataframe.iterrows():
            price = float(row.at['close'])
            closes.append(price)
            rsi = RSIStrategy(data=closes, period=RSI_PERIOD, oversold=RSI_OVERSOLD, overbought=RSI_OVERBOUGHT)
            macd = MACDStrategy(data=closes)
            # print(macd.histogram)
            if macd.crossDown() and rsi.isOverBought() and in_position:
                in_position = False
                balance = coins * price
                coins = 0
                positions.append(['SELL', price, coins, balance, self.toDatetime(row.at['close_time'])])
                total_trades = total_trades+1
                if(balance > temp_balance):
                    total_win = total_win+1
                else:
                    total_lose = total_lose+1
                temp_balance = balance
            
            if macd.crossUp() and rsi.isOverSold() and not in_position:
                in_position = True
                coins = balance / price
                temp_balance = balance
                balance = 0
                positions.append(['BUY', price, coins, temp_balance, self.toDatetime(row.at['close_time'])])

        # Print position history
        table = tabulate(positions, headers=["Position", "Price", "Coins", "Balance", "Time", 'Time UNIX'], tablefmt="orgtbl")
        print(table)

        # Result
        precentage = round((total_win / (total_win + total_lose)) * 100, 2)
        print("="*10)
        print(f"Total Trade: {total_trades} | Win: {total_win} | Lose: {total_lose} | Precentage: {precentage}% | Final Balance: {round(temp_balance,2)}")


# Runing Backtesting
Yuri().backtesting()

