import yfinance as yf
from yahoo_fin.stock_info import get_holders
import csv
from datetime import *

# Create a CSV file to write the data
with open("IHtoStock.csv", mode="w", newline="") as csv_file:  # Use "w" mode to overwrite the file
    fieldnames = ["Date Reported","StockSymbol", "Top Institutional Holders", "Shares", "Value"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for ticker in ["aapl", "meta", "amzn", "googl", "nvda", "msft", "amd"]:
        try:
            holders = get_holders(ticker)
            if "Top Institutional Holders" in holders:
                top_institutional_holders = holders["Top Institutional Holders"]
                dates = top_institutional_holders["Date Reported"]
                shares = top_institutional_holders["Shares"]
                value = top_institutional_holders["Value"]
                holder = top_institutional_holders["Holder"]

                for date, holder2, shares, value in zip(dates, holder, shares, value):
                    # Parse the input date
                    parsed_date = datetime.strptime(date, '%b %d, %Y')
                    # Format the date as "YYYY-MM-DD"
                    formatted_date = parsed_date.strftime('%Y-%m-%d')

                    writer.writerow({"Date Reported": formatted_date, "StockSymbol": ticker.upper(), "Top Institutional Holders": holder2, "Shares": shares, "Value": value})
        except Exception as e:
            # Handle exceptions or errors here
            print(f"Error for {ticker}: {str(e)}")

print("Data has been written to IHtoStock.csv.")
