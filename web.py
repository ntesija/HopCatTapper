from flask import Flask, jsonify, render_template, url_for
from tapperWeb import getTapperData
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.hopcat
tappedLocations = [
	"ann-arbor",
	# "detroit",
	"east-lansing",
	"chicago",
	"grand-rapids",
	"kalamazoo",
	# "royal-oak"
]

@app.route("/list/<location>")
def home(location):
	collection = db[location]
	data = collection.find()
	return render_template("beer-list.html", beerList=data)

def updateDatabase():
	for location in tappedLocations:
		print(location)
		collection = db[location]
		collection.delete_many({})
		beerList = getTapperData(location)
		collection.insert_many(beerList)

if __name__ == "__main__":
	# updateDatabase()
	app.run(debug=True, threaded=True)