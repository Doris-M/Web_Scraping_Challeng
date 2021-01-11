from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)


@app.route("/")
def index():
    data_mars = mongo.db.data_mars.find_one()
    return render_template("index.html", data_mars = data_mars)


@app.route("/scrape")
def scraper():
    data_mars = mongo.db.data_mars
    mars_data_escraped = scrape_mars.latest_new()
    mars_data_escraped = scrape_mars.featured_img()
    mars_data_escraped = scrape_mars.mars_facts()
    mars_data_escraped = scrape_mars.mars_hemispheres_img()
    
    
    data_mars.update({}, mars_data_escraped, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

  