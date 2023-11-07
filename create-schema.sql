-- Create the Company Entity table
CREATE TABLE Company (
    CompanyID INTEGER PRIMARY KEY,
    CompanyName TEXT,
    StockSymbol TEXT,
    CompanyLocation TEXT,
    Industry TEXT,
    Sector TEXT,
    CEO TEXT
);

-- Create the Stock Exchange Entity table
CREATE TABLE StockExchange (
    ExchangeID INTEGER PRIMARY KEY,
    ExchangeName TEXT NOT NULL,
    ExchangeLocation TEXT,
    TradingHours TEXT
);

-- Create the Stock Entity table
CREATE TABLE Stock (
    StockSymbol TEXT PRIMARY KEY,
    CompanyName TEXT NOT NULL,
    CurrentPrice DECIMAL(10, 2) NOT NULL,
    DividendYield DECIMAL(10, 2) NOT NULL,
    StockExchange TEXT,
    FOREIGN KEY (StockSymbol) REFERENCES Company(StockSymbol),
    FOREIGN KEY (StockExchange) REFERENCES StockExchange(ExchangeName)
);

-- Create the News Entity table
CREATE TABLE News (
    NewsID INTEGER PRIMARY KEY,
    Name TEXT,
    Source TEXT,
    Publisher TEXT,
    Thumbnail BLOB,
    StockSymbol TEXT,
    RelatedStocks TEXT
);

-- Create the Stock Index Entity table
CREATE TABLE StockIndex (
    IndexID INTEGER PRIMARY KEY,
    IndexName TEXT NOT NULL
);

-- Create the Stock to News (many-to-many) relationship table
CREATE TABLE StockToNews (
    NewsID INTEGER,
    StockSymbol TEXT,
    FOREIGN KEY (StockSymbol) REFERENCES Stock(StockSymbol),
    FOREIGN KEY (NewsID) REFERENCES News(NewsID),
    PRIMARY KEY (StockSymbol, NewsID)
);

-- Create the Stock to Index (many-to-many) relationship table
CREATE TABLE StockToIndex (
    IndexID INTEGER,
    StockSymbol TEXT,
    FOREIGN KEY (StockSymbol) REFERENCES Stock(StockSymbol),
    FOREIGN KEY (IndexID) REFERENCES StockIndex(IndexID),
    PRIMARY KEY (StockSymbol, IndexID)
);

-- Create the Institutional Holders Entity table
CREATE TABLE InstitutionalHolders (
    Holder TEXT PRIMARY KEY
);

-- Create the Stock to Institutional Holders (many-to-many) relationship table
CREATE TABLE StockToInstitutionalHolders (
    Date DATE,
    StockSymbol TEXT,
    Holder TEXT,
    Shares INTEGER,
    Value INTEGER,
    FOREIGN KEY (StockSymbol) REFERENCES Stock(StockSymbol),
    FOREIGN KEY (Holder) REFERENCES InstitutionalHolders(Holder),
    PRIMARY KEY (StockSymbol, Holder)
);

-- Create the StockPrices table with a foreign key reference to Stock
CREATE TABLE StockPrices (
    Date DATE NOT NULL,
    StockSymbol TEXT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Volume INTEGER NOT NULL,
    FOREIGN KEY (StockSymbol) REFERENCES Stock(StockSymbol), -- Assuming CompanyName corresponds to StockSymbol
    PRIMARY KEY (Date, StockSymbol)
);
