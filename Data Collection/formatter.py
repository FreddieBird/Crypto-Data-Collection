## formats cryptodatadownload csv's into ccxt pulled data format

from datetime import datetime
import pandas as pd
import csv
import os
import numpy as np

exchange = 'binance'
timeframe = '1m'
#symbols = ['ADA-PERP', 'ALT-PERP', 'BCH-PERP', 'BNB-PERP', 'BTC-PERP', 'DEFI-PERP', 'DOT-PERP', 'EOS-PERP', 'EXCH-PERP', 'ETH-PERP', 'FTT-PERP', 'HOLY-PERP', 'KSM-PERP', 'LINK-PERP', 'LTC-PERP', 'SHIT-PERP', 'SOL-PERP', 'SRM-PERP', 'SUSHI-PERP', 'TRX-PERP', 'UNI-PERP', 'XRP-PERP']
symbols = ['ADA/USDT', 'BNB/USDT', 'BTC/USDT', 'DOT/USDT', 'EOS/USDT', 'ETH/USDT', 'KSM/USDT', 'LINK/USDT', 'LTC/USDT', 'NANO/USDT', 'NEO/USDT', 'TRX/USDT', 'XLM/USDT', 'XRP/USDT']
for sym in symbols:
    try:
        pair1 = sym.split('/')[0]
        pair2 = sym.split('/')[1]
        print(pair1, pair2)
        csv_path = f"{exchange}/{timeframe}/{exchange}_{pair1}{pair2}_{timeframe}.csv"
        df = pd.read_csv(csv_path)

        df["Time"] = pd.to_datetime(df["date"], dayfirst=True)
        df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df["Symbol"] = df["symbol"]
        df['Open'] = df['open'].astype(np.float64)
        df['High'] = df['high'].astype(np.float64)
        df['Low'] = df['low'].astype(np.float64)
        df['Close'] = df['close'].astype(np.float64)
        df['Volume'] = df['Volume USDT'].astype(np.float64)
        df.drop(['unix', 'date', f'Volume {pair1}', 'open', 'high', 'low', 'close', 'Volume USDT', 'symbol', 'tradecount'], axis='columns', inplace=True)

        df.set_index('Time', inplace=True)
        df = df.iloc[::-1]
        print(df.head())
        df.to_csv(csv_path)
    except Exception as e:
        print(e)
