from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
  dict_scrape = mongo.db.dict_scrape.find_one()
  
  return render_template("index.html", dict_scrape=dict_scrape)

@app.route("/scrape")
def scrape():
  dict_scrape = mongo.db.dict_scrape
  mars_dict_scrape = scrape_mars.scrape()

  dict_scrape.update({}, mars_dict_scrape, upsert=True)

  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)