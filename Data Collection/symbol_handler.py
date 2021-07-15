## Manages the symbols to pull data for.
import csv
import textwrap
from exchange_tickers import BINANCE_TICKERS, FTX_TICKERS

tickers = {'binance': BINANCE_TICKERS, 'ftx': FTX_TICKERS}


class SymbolList:

    def __init__(self, **kwargs):
            self.symbols = kwargs.get("symbols")
            self.exchange = kwargs.get("exchange")

            # for auto mode, use all available tickers
            # for the particular exchange
            if self.symbols == 'auto':
                self.symbols = tickers[self.exchange.name]
            elif self.symbols == None:
                self.symbols = []


    def input_symbol(self, symbol):
        """
        Checks symbol is valid and then adds it to list.
        """
        try:
            self.exchange.connection.fetch_ticker(symbol)
            self.add_symbol(symbol)
        except Exception as e:
            print(e)
            print(f"{symbol} does not exist on {self.exchange.name}!")


    def add_symbol(self, symbol):
        """
        Adds new symbol to exchange_tickers
        and writes to exchange_tickers.py
        if it wasn't already in there.
        """
        self.exchange.connection.fetch_ticker(symbol)
        self.symbols.append(symbol)

        if symbol not in tickers[self.exchange.name]:
            tickers[self.exchange.name].append(symbol)
            with open('exchange_tickers.py', 'w') as f:
                f.write(textwrap.dedent(f"""BINANCE_TICKERS = {tickers['binance']}\nFTX_TICKERS = {tickers['ftx']}"""))
