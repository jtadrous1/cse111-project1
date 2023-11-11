from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from models import Company, Stock, News

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.sqlite'
app.secret_key = '13ZC46AD79QR28XW'  # Set a secret key for flash messages

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def search_company():
    company_results = None
    stock_results = None
    news_results = None

    if request.method == 'POST':
        search_query = request.form['search_query']
        company_results = db.session.query(Company).filter(Company.StockSymbol == search_query).first()
        stock_results = db.session.query(Stock).filter(Stock.StockSymbol == search_query).all()
        news_results = db.session.query(News).filter(News.Name.ilike(f'%{search_query}%')).all()

        if company_results is None:
            flash("No results found for the given stock symbol.")
        elif not stock_results and not news_results:
            flash("No results found for the given search query.")
    
    return render_template('search.html', company_results=company_results, stock_results=stock_results, news_results=news_results)

if __name__ == '__main__':
    app.run(debug=True)
