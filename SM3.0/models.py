from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(255))
    StockSymbol = db.Column(db.String(20))
    CompanyLocation = db.Column(db.String(255))
    Industry = db.Column(db.String(255))
    Sector = db.Column(db.String(255))
    CEO = db.Column(db.String(255))

class Stock(db.Model):
    __tablename__ = 'Stock'
    StockSymbol = db.Column(db.String(20), primary_key=True)
    CompanyName = db.Column(db.String(255))
    CurrentPrice = db.Column(db.Float)
    DividendYield = db.Column(db.Float)
    StockExchange = db.Column(db.String(255))

class News(db.Model):
    __tablename__ = 'News'
    NewsID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Source = db.Column(db.String(255))
    Publisher = db.Column(db.String(255))
    StockSymbol = db.Column(db.String(20))
    RelatedStocks = db.Column(db.String(255))