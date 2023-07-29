import tkinter as tk
import time
import pandas as pd
import sys
import threading
sys.path.append("./")
from main.model.bjs import bjerksund_stensland
import yfinance as yf
import datetime as dt

buy_threshold = 0.9
sell_threshold = 1.1

# Define the ticker symbol and expiration date for the option
ticker = "AAPL"
expiration = "2024-06-21"

# Fetch the option chain for the ticker and expiration date
option_chain = yf.Ticker(ticker).option_chain(expiration)

# Filter the option chain to find the option with the desired strike price
option = option_chain.calls[option_chain.calls.strike == 150.0]

# Calculate the time to expiry for the selected option
expiry_date = dt.datetime.strptime(expiration, "%Y-%m-%d").date()
today = dt.date.today()
time_to_expiry = (expiry_date - today).days / 365

# Retrieve the last price for the selected option
last_price = option["lastPrice"].iloc[-1]
last_trade_date = option["lastTradeDate"].iloc[-1]

# print(f"Last price for AAPL {time_to_expiry:.2f}-year {option.option_type.iloc[0].lower()} option with strike {option.strike.iloc[0]}: {last_price}")
def check_market(ticker):
    aapl = yf.Ticker(ticker)
    stock_price = aapl.history(period="1d")["Close"].iloc[-1]
    strike_price = 150.0
    risk_free_rate = 0.015
    dividend_yield = -0.0116
    time_to_maturity = time_to_expiry
    volatility = 0.25
    
    theoretical_value = bjerksund_stensland(stock_price, strike_price, risk_free_rate, dividend_yield, time_to_maturity, volatility)
    
    # Check if the market value is above the sell threshold
    if last_price > theoretical_value * sell_threshold:
        signal = "SELL"
    # Check if the market value is below the buy threshold
    elif theoretical_value < buy_threshold * last_price:
        signal = "BUY"
    else:
        signal = None
        
    return signal, theoretical_value, last_price, last_trade_date

# Define the function to run the trading bot
def run_bot():
    # Replace this code with actual trading bot code
    print("Trading bot is running...")
    while True:
        signal, theoretical_value, last_price, last_trade_date = check_market()
        if signal is not None:
            print("Theoretical value is: ", theoretical_value)
            print("Last traded price is: ", last_price, " at time", last_trade_date)
            print("Signal generated:", signal)
            # Replace this code with your actual trading code
            # Here, we just print the signal as an example
        time.sleep(10)  # Wait for 1 minute before checking the market again

def start_bot():
    # TODO STUDY IMPACT OF THREADING
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
# Create the GUI window
root = tk.Tk()
root.title("Trading Bot")

# Add a label and text box for the input parameter
input_label = tk.Label(root, text="Enter the threshold value:")
input_label.pack()
input_text = tk.Entry(root)
input_text.pack()
val = input_text.get()

def get_threshold_value():
    threshold_value = input_text.get()
    print(threshold_value)


# Add a button to run the bot
button = tk.Button(root, text="Run Bot", command=get_threshold_value)
button.pack()

# Start the GUI event loop
root.mainloop()