from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.sqlite'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(255))
    StockSymbol = db.Column(db.String(20))
    CompanyLocation = db.Column(db.String(255))
    Industry = db.Column(db.String(255))
    Sector = db.Column(db.String(255))
    CEO = db.Column(db.String(255))
    CurrentPrice = db.Column(db.Float) 
    DividendYield = db.Column(db.Float)  
    Volume = db.Column(db.Integer)

@app.route('/', methods=['GET', 'POST'])
def search_company():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = Company.query.filter(Company.StockSymbol == search_query).all()
        if not results:
            flash("No results found for the given stock symbol.")
    else:
        results = []

    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.secret_key = '13ZC46AD79QR28XW'  # Set a secret key for flash messages
    app.run(debug=True)
