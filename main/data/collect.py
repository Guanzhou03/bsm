from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import sys
sys.path.append("./")
from main.model.BSM import *

strike_price = 455
ticker = "SPY"
expiry = "23-07-2023"
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()
today = datetime.now()

# Retrieve the historical stock price data using yfinance
df = yf.download(ticker, start=start_date, end=end_date)

df = df.sort_values(by="Date")
df = df.dropna()
df = df.assign(close_day_before=df.Close.shift(1))
df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)

sigma = np.sqrt(252) * df['returns'].std()
treasury_ticker = "^TNX"

# Retrieve the historical data for the 10-year US Treasury bond
dfTreasury = yf.download(treasury_ticker, period="1y")

# Get the most recent yield value
risk_free_rate = dfTreasury.iloc[-1]["Close"] / 100
t = (datetime.strptime(expiry, "%d-%m-%Y") - datetime.utcnow()).days / 365
last_closing_price = df.iloc[-1]["Close"]

print('The Option Price is: ', black_scholes_call(strike_price, last_closing_price, risk_free_rate, t, sigma))
