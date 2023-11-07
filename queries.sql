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
