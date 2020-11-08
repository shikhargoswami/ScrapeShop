from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from scrape import scrape
from mail import send_mail
import time
import threading

app = Flask(__name__)

ENV = 'prod'
curr_price = int()

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://maverick:inmyremains@localhost/postgres'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iaasrmoxakfdmp:49e4f85381ed6d8886132752955ef6a893d2c6941d9a21ee733460c6bc027b28@ec2-54-156-149-189.compute-1.amazonaws.com:5432/dc2fhc0esoffvi'

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
    if request.method == 'POST':
        url = request.form['product']
        price = request.form['price']
        price = int(price)
        email = request.form['email']

        if url == '' or email=='':
            return render_template('index.html', message='Please enter a valid URl or email')

        print(url)
        if db.session.query(Database).filter(Database.email==email).count() ==0:
            
            #event = threading.Event()
            #while(True):
            scraped_name, scraped_price = scrape(url)
            print(scraped_name, scraped_price)
            #event.wait(60*60*60*5)

            if (scraped_price) <= int(price):
                send_mail(email, url)
                #continue
            #else:
                #send_mail(email, url)
                #break
            
            data = Database(url, scraped_name, scraped_price, price, email)
            db.session.add(data)
            db.session.commit()
            
            return render_template('success.html', message='We will notify you when the price drops!', 
                                    email = email, product_name=scraped_name, current_price=scraped_price)

        
        return render_template('index.html', message='You have already asked us to notify for this product')
        
        

if __name__ == '__main__':
    app.run()