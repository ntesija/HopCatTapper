from flask import Flask, jsonify, render_template, url_for
from tapperWeb import getTapperData
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.hopcat

@app.route("/list/<location>")
def home(location):
	collection = db[location]
	data = collection.find()
	return render_template("beer-element.html", beerList=data)

@app.route("/api/v1/beers/<location>", methods=['GET'])
def beers(location):
	return jsonify({'data': render_template('beer-element.html', beerList=getTapperData(location))})

def updateDatabase():
	collection = db['ann-arbor']
	collection.delete_many({})
	beerList = getTapperData("ann-arbor")
	collection.insert_many(beerList)

if __name__ == "__main__":
	updateDatabase()
	app.run(debug=True, threaded=True)