import csv
import yfinance as yf
from yahoo_fin.stock_info import *
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

# important
csv_filename = "stocks-db-3.csv"
txt_filename = "stocks/other.txt"
exch = "New York Stock Exchange"

# Read data from the CSV file
csv_data = []

with open(csv_filename, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csv_data.append(row["StockSymbol"])

# Read data from the TXT file
with open(txt_filename, 'r') as txtfile:
    txt_data = eval(txtfile.read())

# Find and append missing data to the CSV
missing_data = [symbol for symbol in txt_data if symbol not in csv_data]

if missing_data:
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["StockSymbol", "CompanyName", "CurrentPrice", "DividendYield", "StockExchange"])

        for ticker in missing_data:
            stock = yf.Ticker(ticker)
            try:
                info = stock.info
            except requests.exceptions.HTTPError as e:
                # Handle the exception by assigning default values
                info = {}

            name = info.get("longName", "None")
            currentPrice = info.get("currentPrice", 0)
            dividendYield = info.get("trailingAnnualDividendYield", 0)
            exchange = info.get("exchange", exch)

            if exchange in exchange_mapping:
                exchange = exchange_mapping[exchange]

            writer.writerow({
                "StockSymbol": ticker,
                "CompanyName": name,
                "CurrentPrice": currentPrice,
                "DividendYield": round(dividendYield, 2),
                "StockExchange": exchange
            })

print("Missing data appended to the CSV file.")

# Remove data from CSV if it's not in the TXT file
removed_data = [symbol for symbol in csv_data if symbol not in txt_data]

if removed_data:
    updated_csv_data = []
    
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["StockSymbol"] not in removed_data:
                updated_csv_data.append(row)

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["StockSymbol", "CompanyName", "CurrentPrice", "DividendYield", "StockExchange"])
        writer.writeheader()
        writer.writerows(updated_csv_data)

print("Data removed from the CSV file.")
