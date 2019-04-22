import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

@app.route("/scrape")
def scraper():
    mars = scrape_mars.scrape()
    print("----------")     
    db.mars_facts.insert_one(mars)
    return "Here is the scrapped data"

@app.route("/")
def index():
    mars = list(db.mars_facts.find())
    print(mars)
    return render_template("index.html", mars = mars)

if __name__ == "__main__":
        app.run(debug=True)
