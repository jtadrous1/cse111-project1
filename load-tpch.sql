.mode csv
.separator ","
.import data/company/company-db.csv Company
.import data/stockEx/StockExchange.csv StockExchange
.import data/stock/stocks-db-3.csv Stock
.import data/news/news-db.csv News
.import data/stockIndex/IndexID.csv StockIndex
.import data/stockToNews/stock-to-news.csv stockToNews
.import data/stockToIndex/stock-to-index.csv stockToIndex
.import data/instHolders/instHolders.csv InstitutionalHolders
.import data/IHtoStock/IHtoStock.csv StockToInstitutionalHolders
.import data/stockPrices/stock-price.csv StockPrices

-- sqlite3 tpch.sqlite < create-schema.sql
-- sqlite3 tpch.sqlite < load-tpch.sql