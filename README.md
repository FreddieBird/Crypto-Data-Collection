# Crypto-Data-Collection

## Overview
A system that enables the user to retrieve an up-to-date CSV of any cryptocurrency price series of any timeframe. 
Can be run **automatically**, where data is collected for a pre-existing list of crypto symbols, or can be **manually** used to select particular cryptos and timeframes.

Will store the csv in the corresponding folder. E.g. Hourly BTCUSDT from Binance will be stored as "/binance/1h/binance_BTCUSDT_1h.csv".

## How To Use
### get_data_auto_main.py
1) Enter list of exchanges e.g. ['binance', 'ftx'].
2) Set timeframe to pull data for e.g. '1m', '1h', '1d'.
3) In *exchange_tickers.py*, enter the crypto symbols you wish to pull for each exchange.
4) Run.

### get_data_gui.py
1) Start GUI.
2) Enter symbol you wish to collect data for.
3) Choose timeframe.
4) Choose exchange.
5) Run.
6) If the collecte data is for a new symbol, it will be added to the lists in *exchange_tickers.py* - ready to be automatically collected next time.
