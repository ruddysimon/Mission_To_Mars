# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.destination_data.find_one()

    # Return template and data
    return render_template("index.html", destination_data=destination_data)


@app.route("/scrape")
def scrape():
    mars = mongo.db.destination_data
    m_data = scrape_mars.scrape()  
    mars.update({}, m_data, upsert = True)
    return "success"

if __name__ =='__main__':
    app.run(debug=True)   

