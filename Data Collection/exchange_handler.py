import ccxt


class Exchange:

    def __init__(self, exchange_name):
        self.name = exchange_name
        self.connection = self.make_connection()


    def make_connection(self):
        """
        Creates an exchange connection using ccxt.
        Can use all of normal ccxt methods.
        """
        exchange_class = getattr(ccxt, self.name)
        exch = exchange_class({
            'enableRateLimit': True,
        })
        exch.load_markets()
        return exch
