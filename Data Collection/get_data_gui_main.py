## Driver file for GUI data collector
import time
import pytz
from datetime import datetime
from exchange_handler import Exchange
from timeframe_handler import Timeframe
from symbol_handler import SymbolList
from price_data_handler import PriceData
from tkinter import *


BACKGROUND_COLOUR = 'SkyBlue'

EXCHANGE_NAMES = ['binance', 'ftx']
TIMEFRAMES = ['1m', '5m', '1h', '4h', '1d']

"""Empty globals to be filled in by the user using the GUI."""
input_exchange = ""
input_symbols = []
all_symbols = False
input_timeframe = ""
"""Empty globals to be filled in by the user using the GUI."""


def get_data_logic():
    """
    Perform core scraping logic when user presses 'Get Data'.
    """
    global input_exchange
    global input_symbols
    global all_symbols
    global input_timeframe

    # create exchange connection
    exchange = Exchange(input_exchange)

    # perform check that exchange can grab price data
    if exchange.connection.has['fetchOHLCV']:

        # user ticked 'All Symbols?', so includes all symbols in
        # exchange_tickers.py for the particular exchange
        if all_symbols:
            symbol_list = SymbolList(symbols='auto', exchange=exchange)
        # user didn't tick 'All Symbols?', so create unpopulated symbol list
        else:
            symbol_list = SymbolList(exchange=exchange)
        # add all symbols user inputted
        for s in input_symbols:
            symbol_list.input_symbol(s)

        # get auto timeframe and check it is valid
        timeframe = Timeframe(timeframe=input_timeframe, exchange=exchange)
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

        print("Finished writing files!")

def main():
    #Creating a new window and configurations
    window = Tk()
    window.title("Crypto Data Scraper 2000 Platinum Edition")
    window.minsize(width=500, height=500)
    window.config(padx=20, pady=10, bg=BACKGROUND_COLOUR)

    # Select Exchange text
    label_1 = Label(text="Select Exchange", font=("Courier", 8), bg=BACKGROUND_COLOUR)
    label_1.config(padx=10, pady=10)
    label_1.grid(column=0, row=0)

    # Exchange Listbox
    def exchange_listbox_used(event):
        global input_exchange
        # Gets current selection from listbox
        input_exchange = exchange_listbox.get(exchange_listbox.curselection())
        print(input_exchange)

    exchange_listbox = Listbox(height=len(EXCHANGE_NAMES), width=15, bg='snow', exportselection=False)
    for e in EXCHANGE_NAMES:
        exchange_listbox.insert(EXCHANGE_NAMES.index(e), e)
    exchange_listbox.bind("<<ListboxSelect>>", exchange_listbox_used)
    exchange_listbox.grid(column=1, row=0)

    # Select Symbol(s) text
    label_2 = Label(text="Select Symbol(s)", font=("Courier", 8), bg=BACKGROUND_COLOUR)
    label_2.config(padx=10, pady=10)
    label_2.grid(column=0, row=1)

    # Symbol Entry box
    symbol_entry = Entry(width=30, justify='center', bg='snow')
    #Add some text to begin with
    symbol_entry.insert(END, string="")
    symbol_entry.grid(column=1, row=1)

    # Add Symbol Button
    def append_symbol():
        global input_symbols
        input_symbols.append(symbol_entry.get())
        print("Current symbols you will get data for:")
        print(input_symbols)

    button = Button(text="Add Symbol", command=append_symbol, relief=GROOVE, bg='snow')
    button.grid(column=1, row=3)

    # All Symbols text
    label_3 = Label(text="All symbols?", font=("Courier", 8), bg=BACKGROUND_COLOUR)
    label_3.config(padx=10, pady=10)
    label_3.grid(column=0, row=4)

    # All symbols checkbutton
    def checkbutton_used():
        global all_symbols
        #Prints 1 if On button checked, otherwise 0.
        if checked_state.get():
            all_symbols = True
        else:
            all_symbols = False
        print(f"Using all symbols: {all_symbols}")
    #variable to hold on to checked state, 0 is off, 1 is on.
    checked_state = IntVar()
    checkbutton = Checkbutton(text="All Symbols?", variable=checked_state, command=checkbutton_used, bg=BACKGROUND_COLOUR)
    checked_state.get()
    checkbutton.grid(column=1, row=4)

    # Select timeframe text
    label_4 = Label(text="Select timeframe", font=("Courier", 8), bg=BACKGROUND_COLOUR)
    label_4.config(padx=10, pady=10)
    label_4.grid(column=0, row=5)

    # # Timeframe radiobuttons
    # #Radiobutton
    # def radio_used():
    #     print(radio_state.get())
    # #Variable to hold on to which radio button value is checked.
    # radio_state = IntVar()
    # radiobutton1 = Radiobutton(text="1m", value=1, variable=radio_state, command=radio_used)
    # radiobutton2 = Radiobutton(text="5m", value=2, variable=radio_state, command=radio_used)
    # radiobutton3 = Radiobutton(text="1h", value=3, variable=radio_state, command=radio_used)
    # radiobutton4 = Radiobutton(text="4h", value=4, variable=radio_state, command=radio_used)
    # radiobutton5 = Radiobutton(text="1d", value=5, variable=radio_state, command=radio_used)
    # radiobutton1.grid(column=1, row=5)
    # radiobutton2.grid(column=2, row=5)
    # radiobutton3.grid(column=3, row=5)
    # radiobutton4.grid(column=4, row=5)
    # radiobutton5.grid(column=5, row=5)

    # Timeframe listbox
    def timeframe_listbox_used(event):
        # Gets current selection from listbox
        global input_timeframe
        input_timeframe = timeframe_listbox.get(timeframe_listbox.curselection())
        print(input_timeframe)

    timeframe_listbox = Listbox(height=len(TIMEFRAMES), width=15, bg='snow', exportselection=False)
    for tf in TIMEFRAMES:
        timeframe_listbox.insert(TIMEFRAMES.index(tf), tf)
    timeframe_listbox.bind("<<ListboxSelect>>", timeframe_listbox_used)
    timeframe_listbox.grid(column=1, row=5)

    def get_data_button_pressed():
        print(input_exchange, input_symbols, all_symbols, input_timeframe)
        get_data_logic()
    # Get Data Button
    button = Button(text="Get Data",
        command=get_data_button_pressed,
        relief=GROOVE, bg='snow')
    button.grid(column=1, row=6)



    window.mainloop()

if __name__=='__main__':
    main()
