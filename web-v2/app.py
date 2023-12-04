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
from prophet import Prophet
from pandas_datareader import data as  pdr
import datetime as dt
import yfinance as yf
import plotly.express as px


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
    indices = relationship('StockToIndex', back_populates='stock')
    holder = relationship('StockToInstitutionalHolders', back_populates='stock')

class News(db.Model):
    __tablename__ = 'News'
    NewsID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255))
    Source = db.Column(db.String(255))
    Publisher = db.Column(db.String(255))
    Thumbnail = db.Column(db.BLOB)
    StockSymbol = db.Column(db.String(255))
    RelatedStocks = db.Column(db.String(255))

class StockIndex(db.Model):
    __tablename__ = 'StockIndex'
    IndexID = db.Column(db.Integer, primary_key = True)
    IndexName = db.Column(db.String(255))

    stocks = relationship('StockToIndex', back_populates='index')

class StockToIndex(db.Model):
    __tablename__ = 'StockToIndex'
    IndexID = db.Column(db.Integer, db.ForeignKey('StockIndex.IndexID'), primary_key=True)
    StockSymbol = db.Column(db.String(20), db.ForeignKey('Stock.StockSymbol'), primary_key=True)

    stock = relationship('Stock', back_populates='indices')
    index = relationship('StockIndex', back_populates='stocks')

class StockPrice(db.Model):
    __tablename__ = 'StockPrices'
    Date = db.Column(db.String(255), primary_key=True)
    StockSymbol = db.Column(db.String(20), db.ForeignKey('Stock.StockSymbol'))
    Price = db.Column(db.DECIMAL(10, 2))
    Volume = db.Column(db.INTEGER)

class InstitutionalHolders(db.Model):
    __tablename__ = 'InstitutionalHolders'
    Holder = db.Column(db.String(255), primary_key=True)

    stock_holdings = relationship('StockToInstitutionalHolders', back_populates='institutional_holder')

class StockToInstitutionalHolders(db.Model):
    __tablename__ = 'StockToInstitutionalHolders'
    Date = db.Column(db.Date, primary_key=True)
    StockSymbol = db.Column(db.String(20), db.ForeignKey('Stock.StockSymbol'))
    Holder = db.Column(db.String(255), db.ForeignKey('InstitutionalHolders.Holder'))
    Shares = db.Column(db.Integer)
    Value = db.Column(db.Integer)

    stock = relationship('Stock', back_populates='holder')
    institutional_holder = relationship('InstitutionalHolders', back_populates='stock_holdings')


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
        company = Company.query.filter(Company.StockSymbol == symbol).first()
        stock = Stock.query.filter(Stock.StockSymbol == symbol).first()
        news = News.query.filter(News.StockSymbol == symbol).all()
        chart = ""

        if company is not None:
            conn = sqlite3.connect('instance/data.sqlite')

            # Query the data from the SQLite database
            query = f"SELECT Date, Price FROM StockPrices WHERE StockSymbol = '{symbol}'"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                # Fetch stock data using yfinance if the stock data is not in the database
                stock_info = yf.Ticker(symbol)
                hist = stock_info.history(period="5000mo")

                # Save the DataFrame to the database
                for index, row in hist.iterrows():
                    new_date = str(index) + "|" + str(symbol)
                    new_stock_price = StockPrice(Date= new_date, StockSymbol=symbol.upper(), Price=row['Close'], Volume=row['Volume'])
                    db.session.add(new_stock_price)
                db.session.commit()

                # plot stock prices
                df['Date'] = pd.to_datetime(df['Date'].str.split('|').str[0])
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
                chart = base64.b64encode(output.getvalue()).decode('utf-8')
            else:
                # works, but will be very slow
                # stock_info = yf.Ticker(symbol)
                # hist = stock_info.history(period="5000mo")
                
                # for index, row in hist.iterrows():
                #     new_date = str(index) + "|" + str(symbol)

                #     # Check if the data already exists in the database
                #     existing_data = StockPrice.query.filter_by(Date=new_date, StockSymbol=symbol.upper()).first()

                #     if existing_data is None:
                #         # If the data does not exist, add it to the database
                #         new_stock_price = StockPrice(Date=new_date, StockSymbol=symbol.upper(), Price=row['Close'], Volume=row['Volume'])
                #         db.session.add(new_stock_price)
                #         db.session.commit()

                # plot stock prices
                df['Date'] = pd.to_datetime(df['Date'].str.split('|').str[0])
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
                chart = base64.b64encode(output.getvalue()).decode('utf-8')

        return render_template('company-info.html', data=company, data2=stock, data3=news, img_data=chart)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/stock_index')
def stock_index():
    try:
        index = StockIndex.query.all()
        return render_template('stock-index.html', data=index)
    except Exception as e:
        return render_template('stock-index.html')

@app.route('/stock_exchange')
def stock_exchange():
    try:
        ex = StockExchange.query.all()
        stock = Stock.query.all()
        return render_template('stock-exchange.html', data=ex, data2=stock)
    except Exception as e:
        return render_template('stock-exchange.html')
    
@app.route('/analytics')
def analytics():
    try:
        return render_template('analytics.html')
    except Exception as e:
        return render_template('analytics.html', error=str(e))
    
@app.route('/analytics/<symbol>', methods=['GET'])
def analytics2(symbol):
    try:
        # start = dt.datetime(2000, 1, 1)
        start = dt.datetime.now() - dt.timedelta(days=1825)
        end = dt.datetime.now()

        yf.pdr_override()

        info = yf.download(symbol, start, end)
        info.to_csv("stock.csv")

        data = pd.read_csv("stock.csv")
        data = data[["Date", "Close"]]
        data.columns = ["ds", "y"]

        prophet = Prophet(daily_seasonality=True)
        prophet.fit(data)

        future_date = prophet.make_future_dataframe(periods=365)
        predictions = prophet.predict(future_date)

        # Concatenate actual prices with predicted prices
        merged_data = pd.concat([data.set_index('ds')['y'], predictions.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]], axis=1)

        fig = px.line(merged_data, x=merged_data.index, y=['y', 'yhat'], title=f'{symbol} Stock Prediction')

        # Set legend labels
        fig.for_each_trace(lambda t: t.update(name='Actual') if t.name == 'y' else t.update(name='Predicted'))

        # Convert the Plotly figure to HTML
        plot_html = fig.to_html(full_html=False)

        return render_template('analytics.html', plot_html=plot_html)

    except Exception as e:
        return render_template('analytics.html', error=str(e))

@app.route('/holder')
def holder():
    try:
        holder = InstitutionalHolders.query.all()
        stock_holders = StockToInstitutionalHolders.query.all()
        return render_template('holder.html', data=holder, data2=stock_holders)
    except Exception as e:
        return render_template('holder.html', error=str(e))

@app.route('/get_all_stock_to_institutional_data', methods=['GET'])
def get_all_stock_to_institutional_data():
    try:
        stock_to_institutional_data = StockToInstitutionalHolders.query.all()

        data = [{
            "Date": entry.Date,
            "StockSymbol": entry.StockSymbol,
            "Holder": entry.Holder,
            "Shares": entry.Shares,
            "Value": entry.Value
        } for entry in stock_to_institutional_data]

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/get_stocks_in_index/<index_id>', methods=['GET'])
def get_stocks_in_index(index_id):
    # Query the database to retrieve stocks associated with the selected index
    stocks_in_index = StockToIndex.query.filter_by(IndexID=index_id).all()
    indexData = [{"StockSymbol": stock_in_index.StockSymbol} for stock_in_index in stocks_in_index]

    # Render a template with the stocks data
    return jsonify(indexData)

# gets ALL company data in json form
@app.route('/get_all_company_data', methods=['GET'])
def get_all_data():
    try:
        companies = Company.query.all()

        company_data = [{"CompanyID": company.CompanyID, "CompanyName": company.CompanyName, "StockSymbol": company.StockSymbol, "CompanyLocation": company.CompanyLocation, "Industry": company.Industry, "Sector": company.Sector, "CEO": company.CEO} for company in companies]

        return jsonify(company_data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
# adding stocks to index 
@app.route('/add')
def add_stock_symbols_to_index():
    stock_symbols = ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']

    # Insert stock symbols into the StockToIndex table if not already present
    for symbol in stock_symbols:
        if not StockToIndex.query.filter_by(IndexID=2, StockSymbol=symbol).first():
            stock_to_index_entry = StockToIndex(IndexID=2, StockSymbol=symbol)
            db.session.add(stock_to_index_entry)

    db.session.commit()

    return "Stock symbols added to StockToIndex table"

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