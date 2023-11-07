import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import json

dow = tickers_dow()
nasdaq = tickers_nasdaq()
sp500 = tickers_sp500()
other = tickers_other()

exchange_mapping = {
    "ASE": "New York Stock Exchange",
    "BTS": "New York Stock Exchange",
    "NYQ": "New York Stock Exchange",
    "PCX": "New York Stock Exchange",
    "YHD": "New York Stock Exchange",
    "NGM": "Nasdaq",
    "NCM": "Nasdaq",
    "NMS": "Nasdaq",
}

lists = {
    "dow": (dow, "Dow Jones"),
    "nasdaq": (nasdaq, "NASDAQ"),
    "sp500": (sp500, "S&P 500"),
    "other": (other, "Other Exchange")
}

def switch(argument):
    if argument in lists:
        return lists[argument]
    else:
        return None

# Create a CSV file to write the data
with open("stocks-db-3.csv", mode="a", newline="") as csv_file:
    fieldnames = ["StockSymbol", "CompanyName", "CurrentPrice", "DividendYield", "StockExchange"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for key in ["other"]:
        data = switch(key)
        if data:
            stocks, source = data

            # if timeout error change stocks -> stocks[:]
            for ticker in stocks:
                stock = yf.Ticker(ticker)

                try:
                    info = stock.info
                except requests.exceptions.HTTPError as e:
                    pass

                name = info.get("longName", "None")
                currentPrice = info.get("currentPrice", 0)
                dividendYield = info.get("trailingAnnualDividendYield", 0)
                exchange = info.get("exchange", "None")

                # Initialize divYieldPercent to None
                divYieldPercent = None

                if dividendYield != "None" and dividendYield is not None:
                    divYieldPercent = float(dividendYield) * 100

                if exchange in exchange_mapping:
                    exchange = exchange_mapping[exchange]

                # Write data to CSV
                writer.writerow({
                    "StockSymbol": ticker,
                    "CompanyName": name,
                    "CurrentPrice": currentPrice,
                    "DividendYield": round(divYieldPercent, 2),
                    "StockExchange": exchange
                })
