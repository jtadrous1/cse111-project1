-- sqlite3 tpch.sqlite < queries.sql > output.txt

-- Query 1
-- gets companies based in US
SELECT 'Query 1: --------------------------------------------------------';
.headers on
SELECT * FROM Company
WHERE CompanyLocation LIKE "%United States%"
LIMIT 5;
.headers off

SELECT '';

-- Query 2
-- gets companies where stock price over $450
SELECT 'Query 2: --------------------------------------------------------';
.headers on
SELECT * FROM Stock
WHERE CurrentPrice > 450
LIMIT 5;
.headers off

SELECT '';

-- Query 3
-- insert stock index
SELECT 'Query 3: --------------------------------------------------------';
INSERT INTO StockIndex (IndexID, IndexName) 
VALUES (4, 'Index4');
.headers off

SELECT '';

-- Query 4
-- delete stock index
SELECT 'Query 4: --------------------------------------------------------';
DELETE FROM StockIndex 
WHERE IndexName = 'Index4';
.headers off

SELECT '';

-- Query 5
-- get prices for AAPL in 2023
SELECT 'Query 5: --------------------------------------------------------';
.headers on
SELECT * FROM StockPrices
JOIN Stock on StockPrices.StockSymbol = Stock.StockSymbol
WHERE 
    Stock.StockSymbol = "AAPL"
    AND
    StockPrices.Date > "2023%"
LIMIT 5;
.headers off

SELECT '';

-- Query 6
-- get stocks that are being held by vanguard
SELECT 'Query 6: --------------------------------------------------------';
.headers on
SELECT DISTINCT (Stock.StockSymbol) FROM Stock
JOIN StockToInstitutionalHolders as stih on stih.StockSymbol = Stock.StockSymbol
WHERE
    stih.Holder LIKE "Vanguard%"
LIMIT 5;
.headers off

SELECT '';

-- Query 7
-- gets the news article that are related to AAPL and GOOGL
SELECT 'Query 7: --------------------------------------------------------';
.headers on
SELECT News.Name FROM News
WHERE News.RelatedStocks Like ("%AAPL% %GOOGL%")
LIMIT 5;
.headers off

SELECT '';

-- Query 8
-- update index name
SELECT 'Query 8: --------------------------------------------------------';
UPDATE StockIndex
SET IndexName = "S&P 500"
WHERE IndexID = 1;
.headers off

SELECT '';

-- Query 9
-- gets the stock symbols that have indexid 1
SELECT 'Query 9: --------------------------------------------------------';
.headers on
SELECT StockToIndex.StockSymbol FROM StockIndex
JOIN StockToIndex on StockToIndex.IndexID =  StockIndex.IndexID
WHERE StockIndex.IndexID = 1
LIMIT 5;
.headers off

SELECT '';

-- Query 10
-- get stocks that have a vanguard holder that own 1M+ shares
SELECT 'Query 10: --------------------------------------------------------';
.headers on
SELECT DISTINCT Stock.StockSymbol, stih.Holder, stih.Shares
FROM StockToInstitutionalHolders AS stih
JOIN Stock ON stih.StockSymbol = Stock.StockSymbol
WHERE 
    stih.Holder LIKE 'Vanguard%'
    AND 
    Shares > 100000000
LIMIT 5;
.headers off

SELECT '';

-- Query 11
-- get stock price between 2020 and 2021 when price over $100
SELECT 'Query 11: --------------------------------------------------------';
.headers on
SELECT * FROM StockPrices
WHERE 
    StockPrices.Date < "2022%"
    AND
    StockPrices.Date >= "2020%"
    AND
    StockPrices.Price > 100
LIMIT 5;
.headers off

SELECT '';

-- Query 12
-- gets the companies being held in vanguard and in the Dow
SELECT 'Query 12: --------------------------------------------------------';
.headers on
SELECT DISTINCT Company.CompanyName, StockIndex.IndexName FROM Stock
JOIN Company on Company.StockSymbol = Stock.StockSymbol
JOIN StockToInstitutionalHolders as stih ON stih.StockSymbol = Stock.StockSymbol
JOIN StockToIndex ON StockToIndex.StockSymbol = Stock.StockSymbol
JOIN StockIndex ON StockIndex.IndexID = StockToIndex.IndexID
WHERE
    stih.Holder LIKE "Vanguard%"
    AND
    StockIndex.IndexName LIKE "Dow%"
LIMIT 5;
.headers off

SELECT '';

-- Query 13
-- get the stocks that are in more than 1 index
SELECT 'Query 13: --------------------------------------------------------';
.headers on
SELECT Stock.StockSymbol, Company.CompanyName
FROM Stock
JOIN Company ON Stock.StockSymbol = Company.StockSymbol
JOIN StockToIndex ON Stock.StockSymbol = StockToIndex.StockSymbol
GROUP BY Stock.StockSymbol, Company.CompanyName
HAVING COUNT(StockToIndex.IndexID) > 1
LIMIT 5;
.headers off

SELECT '';

-- Query 14
-- gets the average value held by all holders of a stock
SELECT 'Query 14: --------------------------------------------------------';
.headers on
SELECT StockSymbol, AVG(Value) AS AverageValue
FROM StockToInstitutionalHolders
GROUP BY StockSymbol
LIMIT 5;
.headers off

SELECT '';

-- Query 15
-- gets the max value held by all holders of a stock
SELECT 'Query 15: --------------------------------------------------------';
.headers on
SELECT StockSymbol, MAX(Value) AS AverageValue
FROM StockToInstitutionalHolders
GROUP BY StockSymbol
LIMIT 5;
.headers off

SELECT '';

-- Query 16
-- counts the news articles written for a stock
SELECT 'Query 16: --------------------------------------------------------';
.headers on
SELECT StockSymbol, COUNT(NewsID) FROM News
GROUP BY StockSymbol
LIMIT 5;
.headers off

SELECT '';

-- Query 17
-- counts how many of a stock contain AAPL
SELECT 'Query 17: --------------------------------------------------------';
.headers on
SELECT COUNT(*)
FROM News
WHERE RelatedStocks LIKE '%AAPL%'
LIMIT 5;
.headers off

SELECT '';

-- Query 18
-- gets the date where volume over 1B
SELECT 'Query 18: --------------------------------------------------------';
.headers on
SELECT Date FROM StockPrices
WHERE Volume > 1000000000
LIMIT 5;
.headers off

SELECT '';

-- Query 19
-- gets the stocks where div yield > 0, in tech, and in the US
SELECT 'Query 19: --------------------------------------------------------';
.headers on
SELECT Stock.StockSymbol, Stock.DividendYield FROM Stock
JOIN Company ON Company.StockSymbol = Stock.StockSymbol
WHERE 
    Stock.DividendYield > 0
    AND
    Company.CompanyLocation LIKE ("%United States%")
    AND
    Company.Sector = "Technology"
LIMIT 5;
.headers off

SELECT '';    

-- Query 20
-- gets the number of ceos that are dr.
SELECT 'Query 20: --------------------------------------------------------';
.headers on
SELECT COUNT(*) FROM Company
WHERE Company.CEO LIKE "%Dr.%"
LIMIT 5;
.headers off