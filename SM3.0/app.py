from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'  # Replace with your database URL
db = SQLAlchemy(app)

# Add this line to display the database URI
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])


class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(255))
    StockSymbol = db.Column(db.String(20))
    CompanyLocation = db.Column(db.String(255))
    Industry = db.Column(db.String(255))
    Sector = db.Column(db.String(255))
    CEO = db.Column(db.String(255))

@app.route('/', methods=['GET', 'POST'])
def search_company():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = Company.query.filter(Company.CompanyName.ilike(f'%{search_query}%')).all()
        print("Search Results:")
        for result in results:
            print(result)
    else:
        results = []

    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
