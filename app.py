from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from scrape import User
import time
import threading
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv('.env')

ENV = 'prod'

users = []
i = 0

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(CRED_DEV)

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(CRED_PROD)
    
app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False

# IMPLEMENT DATABASE

db = SQLAlchemy(app)

class Database(db.Model):
    __tablename__ = 'ScrapeShop'
    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(2048))
    product_name = db.Column(db.String(200)) # Scrape Title
    current_price = db.Column(db.Integer) # Scrape Price(Live)
    exp_price = db.Column(db.Integer)
    email = db.Column(db.String(200))
    

    def __init__(self, product_url, product_name, current_price, exp_price, email):
        self.product_url = product_url
        self.product_name = product_name
        self.current_price = current_price
        self.exp_price = exp_price
        self.email = email


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global i 
    if request.method == 'POST':
        url = request.form['product']
        price = request.form['price']
        price = int(price)
        email = request.form['email']

        if url == '' or email=='':
            return render_template('index.html', message='Please enter a valid URl or email')

        
        if db.session.query(Database).filter(Database.email==email, Database.product_url==url).count() ==0:
            
            users.append(User(email, url, price))
            scraped_name, scraped_price= users[i].scrape()
            i = i+1
            data = Database(url, scraped_name, scraped_price, price, email)
            db.session.add(data)
            db.session.commit()
            
            return render_template('success.html', message='We will notify you when the price drops!', 
                                    email = email, product_name=scraped_name, current_price=scraped_price
                                    , expected_price=price)

        
        return render_template('index.html', message='You have already asked us to notify for this product')
        
        

if __name__ == '__main__':
    app.run()