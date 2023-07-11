from scipy.stats import norm
import numpy as np

def black_scholes_call(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    call_price = S * N_d1 - K * np.exp(-r * T) * N_d2
    return call_price

import numpy as np
from scipy.stats import norm

def bjerksund_stensland(S, K, r, q, T, sigma, is_call=True):
    """
    Computes the price of an American option using the Bjerksund-Stensland model.

    Parameters:
    S (float):      the current stock price
    K (float):      the strike price of the option
    r (float):      the risk-free interest rate
    q (float):      the continuous dividend yield
    T (float):      the time to maturity of the option (in years)
    sigma (float):  the annualized volatility of the stock returns
    is_call (bool): whether the option is a call option (True) or a put option (False)

    Returns:
    float: the price of the American option
    """
    # Check if any input values are non-positive or zero
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan

    # Calculate the parameters of the Bjerksund-Stensland model
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    beta = (0.5 - (r - q) / sigma**2) + np.sqrt((r - q)**2 / sigma**4 + 2 * r / sigma**2)
    B = beta / (beta - 1) * K
    B1 = np.log(B**2 / (S * K)) / (sigma * np.sqrt(T)) + (r - q + beta * sigma) * T / (beta * sigma)
    B2 = np.log(B**2 / (S * K)) / (sigma * np.sqrt(T)) + (r - q - beta * sigma) * T / (beta * sigma)
    A1 = (r - q + beta * sigma) / 2
    A2 = (r - q - beta * sigma) / 2

    # Calculate the early exercise boundary
    if is_call:
        K_star = B - (B - K) * np.exp(A2 * T) if S >= B else \
                 K if S <= K else \
                 B - (B - K) * (S / B)**A1 * np.exp(-B1 * T)
    else:
        K_star = B + (K - B) * np.exp(A2 * T) if S <= B else \
                 K if S >= K else \
                 B + (K - B) * (S / B)**A1 * np.exp(-B1 * T)

    # Calculate the option price
    if S >= K_star:
        if is_call:
            return S - K
        else:
            return K - S
    else:
        h1 = (np.log(S / K_star) + B1 * T) / (sigma * np.sqrt(T))
        h2 = (np.log(S / K_star) + B2 * T) / (sigma * np.sqrt(T))
        if is_call:
            return S * norm.cdf(d1) - K * norm.cdf(d2) + (K - K_star) * np.exp(-r * T) * norm.cdf(h1) - \
                   (S - K_star) * np.exp(-q * T) * norm.cdf(h2)
        else:
            return K * norm.cdf(-d2) - S * norm.cdf(-d1) + (K_star - K) * np.exp(-r * T) * norm.cdf(-h1) - \
                   (K_star - S) * np.exp(-q * T) * norm.cdf(-h2)
                   
