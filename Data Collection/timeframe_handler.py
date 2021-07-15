from timeframes import TIMEFRAMES

## Manages timeframe data and performs exchange checks

class Timeframe:

    def __init__(self, **kwargs):
        self.timeframes = TIMEFRAMES
        self.tf = kwargs.get("timeframe")
        self.exchange = kwargs.get("exchange")


    def check_timeframe(self):
        """
        Checks if timeframe is valid both locally and externally.
        """
        if self.tf not in self.exchange.connection.timeframes:
            print(f"{self.tf} not supported by {self.exchange.name}!")
            return False
        elif self.tf not in self.timeframes:
            print(f"{sefl.tf} not in current folder structure - please create appropriate folder!")
            return False
        else:
            return True


    def input_timeframe(self):
        """
        Asks user to set timeframe and sets this as the object's timeframe.
        """
        tf = input("Please select a timeframe: ")
        self.tf = tf
