import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import json
import ast

dow = tickers_dow()
nasdaq = tickers_nasdaq()
sp500 = tickers_sp500()
other = tickers_other()

# Read the contents of the first file and store them in a list
with open("stocks/nasdaq.txt", "r") as file1:
    file1_contents = [item.strip() for line in file1 for item in ast.literal_eval(line)]

# Read the contents of the second file and store them in a list
with open("stocks/other.txt", "r") as file2:
    file2_contents = [item.strip() for line in file2 for item in ast.literal_eval(line)]

# Iterate through the elements of the first file and insert them into the get_holders function
for item1 in file1_contents:
    try:
        analyst = get_holders(item1)
    except:
        pass
    else:
        pass
    if analyst is not None and "Top Institutional Holders" in analyst:
        analyst_info_df = pd.DataFrame(analyst["Top Institutional Holders"])
        # Save the results to a CSV file in append mode
        analyst_info_df.to_csv("instHolders.csv", index=False, mode="a", header=False)

# Iterate through the elements of the second file and insert them into the get_holders function
for item2 in file2_contents:
    try:
        analyst2 = get_holders(item2)
    except:
        pass
    else:
        pass
    if analyst2 is not None and "Top Institutional Holders" in analyst2:
        analyst_info_df = pd.DataFrame(analyst2["Top Institutional Holders"])
        # Save the results to a CSV file in append mode
        analyst_info_df.to_csv("instHolders.csv", index=False, mode="a", header=False)


# Remove duplicate rows based on the "Holder" column
all_analyst_info_df = analyst_info_df.drop_duplicates(subset=["Holder"])

# all_analyst_info_df.to_csv("instHolders.csv", index=False)

# analyst = get_holders("")
# analyst_info_df = pd.DataFrame(analyst["Top Institutional Holders"])
# analyst_info_df.to_csv("analyst.csv", index=False)