import math
import time
import os
import os.path
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta, timezone
from timeframes import TIMEFRAMES

def fetch_data(exch, exchange, sym, tf, since, utc_offset):
    """
    Given a symbol and timeframe, will pull data from exchange.
    Returns a pandas df.
    """

    data = exch.fetch_ohlcv(sym ,tf, since)
    df = pd.DataFrame(data, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [datetime.fromtimestamp((float(time)-utc_offset)/1000) for time in df['Time']] #df["Time"].astype('datetime64[s]')
    df['Symbol'] = sym
    df['Open'] = df['Open'].astype(np.float64)
    df['High'] = df['High'].astype(np.float64)
    df['Low'] = df['Low'].astype(np.float64)
    df['Close'] = df['Close'].astype(np.float64)
    df['Volume'] = df['Volume'].astype(np.float64)
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.set_index('Time', inplace=True)
    return df


class PriceData:

    def __init__(self, **kwargs):
        self.exchange = kwargs.get("exchange")
        self.timeframe = kwargs.get("tf")
        self.symbol = kwargs.get("sym")
        self.now = kwargs.get("now")
        self.csv_path = kwargs.get("path")
        self.since = kwargs.get("since")
        self.since_displacement = TIMEFRAMES[self.timeframe] 
        self.limit = kwargs.get("limit")
        self.write_header = False
        self.utc_offset = ((datetime.fromtimestamp(time.time()) -
                      datetime.utcfromtimestamp(time.time())).total_seconds())*1000
        self.df_list = []
        self.df_total = pd.DataFrame(columns=["Time", "Symbol", "Open", "High", "Low", "Close", "Volume"])


    def set_since(self, df):
        last_time = datetime.strftime(df.index[-1], "%Y-%m-%d %H:%M:%S")
        last_time = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
        last_time = int(last_time.replace(tzinfo=timezone.utc).timestamp())
        self.since = (last_time*1000) + self.since_displacement


    def exists(self):
        """
        Checks if csv for price data already exists
        in the folder directory.
        """
        return os.path.isfile(self.csv_path)


    def get_current(self):
        """
        Gets current price data from csv and sets 'since'.
        """
        print("Reading from an existing csv!")
        curr_df = pd.read_csv(self.csv_path)
        curr_df.set_index('Time', inplace=True)
        print(curr_df.tail())
        last_time = datetime.strptime(curr_df.index[-1], "%Y-%m-%d %H:%M:%S")
        last_time = int(last_time.replace(tzinfo=timezone.utc).timestamp())
        self.since = (last_time*1000) + self.since_displacement


    def get_new(self):
        """
        Gets new price data from exchange and sets 'since'.
        """
        print("Fetching data for the first time!")
        self.write_header = True
        self.since = None # assume no data exists already
        new_df = fetch_data(self.exchange.connection, self.exchange.name, self.symbol,
                            self.timeframe, self.since, self.utc_offset)
        self.set_since(new_df)
        self.df_list.append(new_df)


    def update(self):
        """
        Keeps scraping data in chunks until now is reached.
        Finally, concatenates all price data together.
        """
        while self.since <= self.now:
            time.sleep(self.exchange.connection.rateLimit / 1000) # stop request limits being reached

            df = fetch_data(self.exchange.connection, self.exchange.name, self.symbol,
                                self.timeframe, self.since, self.utc_offset)
            self.set_since(df)
            self.df_list.append(df)

        # Finally, concat and print
        self.df_total = pd.concat(self.df_list)
        print(self.df_total)


    def write(self):
        """
        Writes the final df to csv.
        In append mode. Will create if csv does not exist.
        """
        self.df_total.to_csv(self.csv_path, mode='a', header=self.write_header)
