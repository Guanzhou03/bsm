import tkinter as tk
import time
import sys
sys.path.append("./")
from main.model.BSM import bjerksund_stensland
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
# print(f"Last price for AAPL {time_to_expiry:.2f}-year {option.option_type.iloc[0].lower()} option with strike {option.strike.iloc[0]}: {last_price}")
def check_market():
    aapl = yf.Ticker("AAPL")
    stock_price = aapl.history(period="1d")["Close"].iloc[-1]
    strike_price = 150.0
    risk_free_rate = 0.015
    dividend_yield = -0.0116
    time_to_maturity = 0.25
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
        
    return signal

# Define the function to run the trading bot
def run_bot():
    # Replace this code with actual trading bot code
    print("Trading bot is running...")
    while True:
        signal = check_market()
        if signal is not None:
            print("Signal generated:", signal)
            # Replace this code with your actual trading code
            # Here, we just print the signal as an example
        time.sleep(1)  # Wait for 1 minute before checking the market again

# Create the GUI window
root = tk.Tk()
root.title("Trading Bot")

# Add a label and text box for the input parameter
input_label = tk.Label(root, text="Enter the threshold value:")
input_label.pack()
input_text = tk.Entry(root)
input_text.pack()

# Add a button to run the bot
button = tk.Button(root, text="Run Bot", command=run_bot)
button.pack()

# Start the GUI event loop
root.mainloop()