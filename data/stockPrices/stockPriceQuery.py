import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import json

dow = tickers_dow()
nasdaq = tickers_nasdaq()
sp500 = tickers_sp500()
other = tickers_other()

for ticker in ["aapl"]:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5000mo")

    hist['Ticker'] = ticker.upper()

    # Save the DataFrame to a CSV file
    hist.to_csv("stock-price.csv", columns=["Ticker", "Close", "Volume"])
    # hist.to_csv("stock-price.csv")