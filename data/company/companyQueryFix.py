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
csv_filename = "company-db.csv"
txt_filename = "stocks/nasdaq.txt"
exch = "Nasdaq"

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
    last_row_index = -1

    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_index, _ in enumerate(reader):
            last_row_index = row_index

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["CompanyID", "CompanyName", "StockSymbol", "CompanyLocation", "Industry", "Sector", "CEO"])

        count = last_row_index
        
        for ticker in missing_data:
            stock = yf.Ticker(ticker)
            try:
                info = stock.info
            except requests.exceptions.HTTPError as e:
                # Handle the exception by assigning default values
                info = {}

            # company entity
            city = info.get("city", "None")
            state = info.get("state", "None")
            country = info.get("country", "None")
            location = country + ", " + state + ", " + city
            sector = info.get("sector", "None")
            name = info.get("longName", "None")
            industry = info.get("industry", "None")

            if "None" in location:
                location = "None"

            if "companyOfficers" in info and info["companyOfficers"] and "name" in info["companyOfficers"][0]:
                ceo = info["companyOfficers"][0]["name"]
            else:
                ceo = "Unknown"
            
            # Write data to CSV
            writer.writerow({
                "CompanyID": count,
                "CompanyName": name,
                "StockSymbol": ticker,
                "CompanyLocation": location,
                "Industry": industry,
                "Sector": sector,
                "CEO": ceo
            })

            count += 1

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
        writer = csv.DictWriter(csvfile, fieldnames=["CompanyID", "CompanyName", "StockSymbol", "CompanyLocation", "Industry", "Sector", "CEO"])
        writer.writeheader()
        writer.writerows(updated_csv_data)

print("Data removed from the CSV file.")