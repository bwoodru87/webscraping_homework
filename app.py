from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data.find()
    mars_data_information = scrape_mars.scrape()
    mars_data.update({}, mars_data_information,upsert=True)
    return redirect("/", code=302)

@app.route("/")
def index():
        mars_data = mongo.db.mars_data
        return render_template("index.html", mars_data=mars_data)


    
if __name__ == "__main__":
        app.run(debug=True)
