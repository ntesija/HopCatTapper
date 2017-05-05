import sys
from flask import Flask, jsonify, render_template, url_for, abort, request
from tapperWeb import getTapperData
from bottleOpenerWeb import getBottleOpenerData
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.hopcat
tappedLocations = []

locations = [
	"ann-arbor",
	# "detroit", # Uses info from Untappd
	"east-lansing",
	"chicago",
	"grand-rapids",
	"kalamazoo",
	# "royal-oak", # Not open yet
	"broad-ripple",
	"kansas-city",
	"lexington",
	"lincoln",
	"louisville",
	"madison"
]

@app.route("/list/<location>")
def home(location):
	notSorted = True
	collection = db[location]
	if collection.count() == 0:
		abort(404)
	data = collection.find()
	typeList = []
	types=[]
	if 'sort' in request.args:
		if request.args.get('sort') == 'type':
			data = sorted(data, key=lambda beer: beer['currentType'])
			count = 1
			for beer in data:
				if beer['currentType'] not in typeList:
					typeList.append(beer['currentType'])
					types.append([beer['currentType'], count])
				count += 1
			notSorted = False
	return render_template("beer-list.html", beerList=data, location=location, tappedLocations=tappedLocations, notSorted=notSorted, types=types)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html", tappedLocations=tappedLocations), 404

def updateDatabase():
	print("Updating database:")
	for location in locations:
		try:
			beerList = getTapperData(location)
			try:
				bottleList = getBottleOpenerData(location)
				data = beerList + bottleList
			except:
				print ("Error getting bottle data for {}".format(location))
				data = beerList
			data = sorted(data, key=lambda beer: beer['ppv'], reverse=True)
			collection = db[location]
			collection.delete_many({})
			collection.insert_many(data)
			tappedLocations.append(location)
		except:
			print("Error getting Tapper data for {}: {}".format(location, sys.exc_info()[0]))

if __name__ == "__main__":
	# updateDatabase()
	tappedLocations = [
		"ann-arbor",
		# "detroit", # Uses info from Untappd
		"east-lansing",
		"chicago",
		"grand-rapids",
		"kalamazoo",
		# "royal-oak", # Not open yet
		"broad-ripple",
		"kansas-city",
		"lexington",
		"lincoln",
		"louisville",
		"madison"
	]
	app.run(debug=True, threaded=True)