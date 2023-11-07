import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import json

dow = tickers_dow()
nasdaq = tickers_nasdaq()
sp500 = tickers_sp500()
other = tickers_other()

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
with open("company-db.csv", mode="a", newline="") as csv_file:
    fieldnames = ["CompanyID", "CompanyName", "StockSymbol", "CompanyLocation", "Industry", "Sector", "CEO"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    count = 5114

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