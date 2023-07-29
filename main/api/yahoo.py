import yfinance as yf
import yahoo_fin.options as op
import sys
sys.path.append("./")
from main.model.bjs import *
import pandas as pd
from datetime import datetime


BUY_THRESHOLD = 0.2
SELL_THRESHOLD = 0.05
RISK_FREE_RATE = 0.02
today = datetime.today()

def get_time_to_expiry(expiration_string):
    # Parse the expiration date string into a datetime object
    expiration_date = datetime.strptime(expiration_string, '%Y-%m-%d')
    # Calculate the time difference between the current date and the expiration date
    time_difference = expiration_date - today 
    # Convert the time difference to a number of days and then to a fraction of a year
    time_to_expiry = time_difference.days / 365.25
    return time_to_expiry

def get_at_the_money_options(ticker, num_dates=20):
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")["Close"].iloc[-1]
    dates = stock.options[:num_dates]
    dfs = []
    for date in dates:
        # exp_date = datetime.strptime(date, '%Y-%m-%d').date()
        # if exp_date < datetime.today().date():
        #     print("SKIPPED")
        #     continue
        options = stock.option_chain(date)
        calls = options.calls
        puts = options.puts
        at_the_money_calls = calls[calls['strike'] >= current_price * 0.95].sort_values(by='strike').head(1)
        at_the_money_puts = puts[puts['strike'] <= current_price * 1.05].sort_values(by='strike').tail(1)
        df = pd.concat([at_the_money_calls, at_the_money_puts], axis=0)
        df['expiration'] = date
        dfs.append(df)
    result = pd.concat(dfs, axis=0)
    return result

# Define a function to determine the buy/sell signal based on the percentage difference
def get_signal(percentage_diff):
    if percentage_diff > 10:
        return "Sell"
    elif percentage_diff < -10:
        return "Buy"
    else:
        return "Hold"
def get_div_yield(ticker):
    ticker = yf.Ticker(ticker)
    dividend_history = ticker.dividends
    most_recent_dividend = dividend_history[-1]
    current_stock_price = ticker.history(period="1d")["Close"].iloc[-1]
    dividend_yield = (most_recent_dividend / current_stock_price)
    return dividend_yield

def getTheoreticalPriceFromOptionDf(df, ticker):

    current_stock_price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]

    df['time_to_expiry'] = df['expiration'].apply(get_time_to_expiry)
    div_yield = get_div_yield(ticker)    
    df['theoretical_price'] = df.apply(lambda row: bjerksund_stensland(current_stock_price, row['strike'], RISK_FREE_RATE, div_yield, row['time_to_expiry'], row['impliedVolatility']), axis=1)

    # Compare the theoretical price with the lastPrice
    df['percentage_diff'] = (df['lastPrice'] - df['theoretical_price']) / df['lastPrice'] * 100
# Apply the get_signal function to each row of the DataFrame
    df['signal'] = df['percentage_diff'].apply(get_signal)

    # Print the DataFrame with the new columns
    print(df)
options_df = get_at_the_money_options("AAPL")
getTheoreticalPriceFromOptionDf(options_df, "AAPL")


