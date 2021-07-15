## Driver file for automatic data collector
import time
import pytz
from datetime import datetime
from exchange_handler import Exchange
from timeframe_handler import Timeframe
from symbol_handler import SymbolList
from price_data_handler import PriceData


EXCHANGE_NAMES = ['binance', 'ftx']
TIMEFRAME = '1m'


def main():
    # create exchange connections
    for e in EXCHANGE_NAMES:
        exchange = Exchange(e)

        # perform check that exchange can grab price data
        if exchange.connection.has['fetchOHLCV']:

            # get auto list of symbols
            symbol_list = SymbolList(symbols='auto', exchange=exchange)

            # get auto timeframe and check it is valid
            timeframe = Timeframe(timeframe=TIMEFRAME, exchange=exchange)
            while not timeframe.check_timeframe():
                timeframe.input_timeframe() # default to asking for input

            print(f"Pulling data on the {timeframe.tf} timeframe for...")
            print(symbol_list.symbols)

            # get current time in UTC in milliseconds
            now = datetime.now().astimezone(pytz.timezone('UTC'))
            now = int(now.timestamp()*1000)

            # loop over each symbol and pull new data
            for sym in symbol_list.symbols:
                # create csv filename and path
                file_sym = sym.replace('/', '')
                file_sym = file_sym.replace('-', '')
                filename = f"{exchange.name}_{file_sym}_{timeframe.tf}.csv" # generate filename from given information
                csv_path = f"{exchange.name}/{timeframe.tf}/{filename}"

                # get most recent price data and append it to existing data
                # (if it exists)
                price_data = PriceData(exchange=exchange, tf=timeframe.tf,
                    sym=sym, now=now, path=csv_path)

                # check if price data csv already exists
                if price_data.exists():
                    price_data.get_current()
                # get new data as far back as possible if csv does not exist
                else:
                    price_data.get_new()

                # keep updating price_data until current time
                price_data.update()

                # write to csv
                price_data.write()


if __name__=='__main__':
    main()
