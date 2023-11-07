-- Query 1
-- gets companies based in US
SELECT * FROM Company
WHERE CompanyLocation LIKE "%United States%";

-- Query 2
-- gets companies where stock price over $450
SELECT * FROM Stock
WHERE CurrentPrice > 450;

-- Query 3
-- insert stock index
INSERT INTO StockIndex (IndexID, IndexName) 
VALUES (4, 'Index4');

-- Query 4
-- delete stock index
DELETE FROM StockIndex 
WHERE IndexName = 'Index4';

-- Query 5
-- get prices for AAPL in 2023
SELECT * FROM StockPrices
JOIN Stock on StockPrices.StockSymbol = Stock.StockSymbol
WHERE 
    Stock.StockSymbol = "AAPL"
    AND
    StockPrices.Date > "2023%";

-- Query 6
-- get stocks that are being held by vanguard
SELECT DISTINCT (Stock.StockSymbol) FROM Stock
JOIN StockToInstitutionalHolders as stih on stih.StockSymbol = Stock.StockSymbol
WHERE
    stih.Holder LIKE "Vanguard%";

-- Query 7
-- gets the news article that are related to AAPL and GOOGL
SELECT News.Name FROM News
WHERE News.RelatedStocks Like ("%AAPL% %GOOGL%");

-- Query 8
-- update index name
UPDATE StockIndex
SET IndexName = "S&P 400"
WHERE IndexID = 1;

-- Query 9
-- gets the stock symbols that have indexid 1
SELECT StockToIndex.StockSymbol FROM StockIndex
JOIN StockToIndex on StockToIndex.IndexID =  StockIndex.IndexID
WHERE StockIndex.IndexID = 1;

-- Query 10
-- get stocks that have a vanguard holder that own 1M+ shares
SELECT DISTINCT Stock.StockSymbol, stih.Holder, stih.Shares
FROM StockToInstitutionalHolders AS stih
JOIN Stock ON stih.StockSymbol = Stock.StockSymbol
WHERE 
    stih.Holder LIKE 'Vanguard%'
    AND 
    Shares > 100000000;

-- Query 11
-- get stock price between 2020 and 2021 when price over $100
SELECT * FROM StockPrices
WHERE 
    StockPrices.Date < "2022%"
    AND
    StockPrices.Date >= "2020%"
    AND
    StockPrices.Price > 100;

-- Query 12
-- gets the companies being held in vanguard and in the Dow
SELECT DISTINCT Company.CompanyName, StockIndex.IndexName FROM Stock
JOIN Company on Company.StockSymbol = Stock.StockSymbol
JOIN StockToInstitutionalHolders as stih ON stih.StockSymbol = Stock.StockSymbol
JOIN StockToIndex ON StockToIndex.StockSymbol = Stock.StockSymbol
JOIN StockIndex ON StockIndex.IndexID = StockToIndex.IndexID
WHERE
    stih.Holder LIKE "Vanguard%"
    AND
    StockIndex.IndexName LIKE "Dow%";

-- Query 13
-- get the stocks that are in more than 1 index
SELECT Stock.StockSymbol, Company.CompanyName
FROM Stock
JOIN Company ON Stock.StockSymbol = Company.StockSymbol
JOIN StockToIndex ON Stock.StockSymbol = StockToIndex.StockSymbol
GROUP BY Stock.StockSymbol, Company.CompanyName
HAVING COUNT(StockToIndex.IndexID) > 1;

-- Query 14
-- gets the average value held by all holders of a stock
SELECT StockSymbol, AVG(Value) AS AverageValue
FROM StockToInstitutionalHolders
GROUP BY StockSymbol;

-- Query 15
-- gets the max value held by all holders of a stock
SELECT StockSymbol, MAX(Value) AS AverageValue
FROM StockToInstitutionalHolders
GROUP BY StockSymbol;

-- Query 16
-- counts the news articles written for a stock
SELECT StockSymbol, COUNT(NewsID) FROM News
GROUP BY StockSymbol;

-- Query 17
-- counts how many of a stock contain AAPL
SELECT COUNT(*)
FROM News
WHERE RelatedStocks LIKE '%AAPL%';

-- Query 18
-- gets the date where volume over 1B
SELECT Date FROM StockPrices
WHERE Volume > 1000000000;

-- Query 19
-- gets the stocks where div yield > 0, in tech, and in the US
SELECT Stock.StockSymbol, Stock.DividendYield FROM Stock
JOIN Company ON Company.StockSymbol = Stock.StockSymbol
WHERE 
    Stock.DividendYield > 0
    AND
    Company.CompanyLocation LIKE ("%United States%")
    AND
    Company.Sector = "Technology";

-- Query 20
-- gets the number of ceos that are dr.
SELECT COUNT(*) FROM Company
WHERE Company.CEO LIKE "%Dr.%"