from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape
from config import mongo_uri

# create the instance of Flask
app = Flask(__name__)

app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_information = mongo.db.mars_information.find_one()
    return render_template("index.html", mars_infoHTML=mars_information)
    
@app.route("/scrape")
def mars_scrape():
    mars_information = mongo.db.mars_information
    mars_data_new = scrape()
    mars_information.update({}, mars_data_new, upsert = True)
    print("db information updated")
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)