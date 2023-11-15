from flask import Flask, request, render_template, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
import json
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import numpy as np
import pandas as pd
import base64
import yfinance as yf
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.secret_key = 'super secret key'
app.app_context().push()
db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(255))
    StockSymbol = db.Column(db.String(20), db.ForeignKey('Stock.StockSymbol'))
    CompanyLocation = db.Column(db.String(255))
    Industry = db.Column(db.String(255))
    Sector = db.Column(db.String(255))
    CEO = db.Column(db.String(255))

    stocks = relationship('Stock', back_populates='company', primaryjoin="Company.StockSymbol == Stock.StockSymbol")

class StockExchange(db.Model):
    __tablename__ = 'StockExchange'
    ExchangeID =  db.Column(db.Integer, primary_key = True)
    ExchangeName =  db.Column(db.String(255))
    ExchangeLocation = db.Column(db.String(255))
    TradingHours = db.Column(db.String(255))

class Stock(db.Model):
    __tablename__ = 'Stock'
    StockSymbol = db.Column(db.String(20), primary_key=True)
    CompanyName = db.Column(db.String(255))
    CurrentPrice = db.Column(db.Float)
    DividendYield = db.Column(db.Float)
    StockExchange = db.Column(db.String(255))

    company = relationship('Company', back_populates='stocks')
    stock_prices = relationship("StockPrice", back_populates="stock")

class StockPrice(db.Model):
    __tablename__ = 'StockPrices'
    Date = db.Column(db.Date, primary_key=True, nullable=False)
    StockSymbol = db.Column(db.INTEGER, db.ForeignKey('Stock.StockSymbol'), primary_key=True, nullable=False)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Volume = db.Column(db.INTEGER, nullable=False)

    stock = relationship("Stock", back_populates="stock_prices", primaryjoin="StockPrice.StockSymbol == Stock.StockSymbol")

class News(db.Model):
    __tablename__ = 'News'
    NewsID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255))
    Source = db.Column(db.String(255))
    Publisher = db.Column(db.String(255))
    Thumbnail = db.Column(db.BLOB)
    StockSymbol = db.Column(db.String(255))
    RelatedStocks = db.Column(db.String(255))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# potential problems:
# * looking up new stocks will take a few seconds to load
# * new stocks wont show graph unless users refresh twice
# * old data
@app.route('/company_info/<symbol>', methods=['GET'])
def company_info(symbol):
    try:
        # Query the database to retrieve the company with the specified stock symbol
        company = Stock.query.filter(Stock.StockSymbol == symbol).first()
        stock = Stock.query.filter(Stock.StockSymbol == symbol).first()
        news = News.query.filter(News.StockSymbol == symbol).all()

        if company is not None:
            conn = sqlite3.connect('instance/data.sqlite')

            # Query the data from the SQLite database
            query = f"SELECT Date, Price FROM StockPrices WHERE StockSymbol = '{symbol}' ORDER BY Date"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                # Fetch stock data using yfinance if the stock data is not in the database
                stock_info = yf.Ticker(symbol)
                hist = stock_info.history(period="5000mo")

                # Save the DataFrame to the database
                for index, row in hist.iterrows():
                    # Check if the record with the same Date and StockSymbol already exists
                    existing_record = StockPrice.query.filter_by(Date=index, StockSymbol=symbol.upper()).first()

                    if existing_record:
                        # If it exists, update the record instead of inserting a new one
                        existing_record.Price = row['Close']
                        existing_record.Volume = row['Volume']
                    else:
                        # If it doesn't exist, insert a new record
                        new_stock_price = StockPrice(Date=index, StockSymbol=symbol.upper(), Price=row['Close'], Volume=row['Volume'])
                        db.session.add(new_stock_price)
                db.session.commit()

                # Plot stock prices
                df['Date'] = pd.to_datetime(df['Date'])
                fig = Figure()
                axis = fig.add_subplot(1, 1, 1)
                xs = df["Date"]
                ys = df['Price']
                axis.plot(xs, ys)
                axis.set_xlabel('Date')
                axis.set_ylabel('Price')
                axis.set_title(f'Stock Price vs. Date for {symbol}')
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
                img_data = base64.b64encode(output.getvalue()).decode('utf-8')
            else:
                # Fetch the latest data from Yahoo Finance
                stock_info = yf.Ticker(symbol)
                hist = stock_info.history(period="1d")

                # Save the latest data to the database
                for index, row in hist.iterrows():
                    new_stock_price = StockPrice(Date=index, StockSymbol=symbol.upper(), Price=row['Close'], Volume=row['Volume'])
                    db.session.add(new_stock_price)
                db.session.commit()

                # Re-fetch the data from the database after updating
                query = f"SELECT Date, Price FROM StockPrices WHERE StockSymbol = '{symbol}' ORDER BY Date"
                df = pd.read_sql_query(query, conn)

                # Plot stock prices
                df['Date'] = pd.to_datetime(df['Date'])
                fig = Figure()
                axis = fig.add_subplot(1, 1, 1)
                xs = df["Date"]
                ys = df['Price']
                axis.plot(xs, ys)
                axis.set_xlabel('Date')
                axis.set_ylabel('Price')
                axis.set_title(f'Stock Price vs. Date for {symbol}')
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
                img_data = base64.b64encode(output.getvalue()).decode('utf-8')

        return render_template('company-info.html', data=company, data2=stock, data3=news, img_data=img_data)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/get_all_company_data', methods=['GET'])
def get_all_data():
    try:
        companies = Company.query.all()

        company_data = [{"CompanyID": company.CompanyID, "CompanyName": company.CompanyName, "StockSymbol": company.StockSymbol, "CompanyLocation": company.CompanyLocation, "Industry": company.Industry, "Sector": company.Sector, "CEO": company.CEO} for company in companies]

        return jsonify(company_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# deprecated 
# @app.route('/plot/<symbol>')
# def plot_png(symbol):
#     conn = sqlite3.connect('instance/data.sqlite')

#     # Query the data from the SQLite database
#     query = f"SELECT Date, Price FROM StockPrices WHERE StockSymbol = '{symbol}'"
#     df = pd.read_sql_query(query, conn)

#     # Convert the 'date' column to datetime format
#     df['Date'] = pd.to_datetime(df['Date'])
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = df["Date"]
#     ys = df['Price']
#     axis.plot(xs, ys)
#     axis.set_xlabel('Date')
#     axis.set_ylabel('Price')
#     axis.set_title(f'Stock Price vs. Date for {symbol}')
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')
    
# @app.route('/get_companies', methods=['GET'])
# def get_company_by_symbol():
#     try:
#         # Extract the 'symbol' query parameter from the request
#         symbol = request.args.get('symbol')

#         if symbol is not None and symbol.strip():  # Check if 'symbol' is not empty
#             # Query the database to retrieve the company with the specified stock symbol
#             company = Company.query.filter(Company.StockSymbol == symbol).first()

#             if company is not None:
#                 # Serialize the data to JSON
#                 company_data = {
#                     "CompanyID": company.CompanyID,
#                     "CompanyName": company.CompanyName,
#                     "StockSymbol": company.StockSymbol,
#                     "CompanyLocation": company.CompanyLocation,
#                     "Industry": company.Industry,
#                     "Sector": company.Sector,
#                     "CEO": company.CEO
#                 }
#                 return jsonify(company_data)
#             else:
#                 return jsonify({"error": "Company not found for the specified symbol"})
#         else:
#             return jsonify({"error": "Symbol parameter is missing or empty in the query"})
#     except Exception as e:
#         return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)