import yfinance as yf
from yahoo_fin.stock_info import *
import csv
import json
import ast
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("instHolders.csv")

# Remove duplicates based on the "Holder" column
df = df.drop_duplicates(subset=["Holder"])

# Drop all columns except "Holder"
df = df.drop(columns=df.columns.difference(["Holder"]))

# Save the deduplicated data back to the CSV file
df.to_csv("instHolders.csv", index=False)
