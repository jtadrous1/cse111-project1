import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import requests

# Create a set to keep track of seen news article names
seen_names = set()

# Create a CSV file to write the data
with open("news-db.csv", mode="a", newline="") as csv_file:
    fieldnames = ["NewsID", "Name", "Source", "Publisher", "Thumbnail", "StockSymbol", "RelatedStocks"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    count = 1

    for ticker in ["aapl", "meta", "amzn", "googl", "nvda", "msft", "amd"]:
        stock = yf.Ticker(ticker)

        try:
            info = stock.news
        except requests.exceptions.HTTPError as e:
            pass
        except requests.exceptions.JSONDecodeError as e:
            pass

        if info is not None:
            # Extract information from all elements in the JSON data
            for item in info:
                title = item.get("title", None)
                # Check if the name has already been added
                if title in seen_names:
                    continue
                seen_names.add(title)

                link = item.get("link", None)
                publisher = item.get("publisher", None)
                thumbnail_url = None
                related_tickers = item.get("relatedTickers", None)

                # Find the 140x140 thumbnail URL
                for resolution in item.get("thumbnail", {}).get("resolutions", []):
                    if resolution.get("tag") == "140x140":
                        thumbnail_url = resolution.get("url")
                        break

                # Write data to CSV for each news item
                writer.writerow({
                    "NewsID": count,
                    "Name": title,
                    "Source": link,
                    "Publisher": publisher,
                    "Thumbnail": thumbnail_url,
                    "StockSymbol": ticker.upper(),
                    "RelatedStocks": ', '.join(related_tickers) if related_tickers else None
                })
                count += 1
