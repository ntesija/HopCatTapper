import threading
from flask import Flask, jsonify, render_template, url_for, abort, request
from pymongo import MongoClient
from updateDatabase import updateLoop
from globals import tappedLocations

app = Flask(__name__)
client = MongoClient()
db = client.hopcat

@app.route("/")
def home():
	return render_template("main.html", tappedLocations=tappedLocations)

@app.route("/list/<location>")
def list(location):
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

if __name__ == "__main__":
	updateThread = threading.Thread(target=updateLoop).start()
	app.run(debug=True, threaded=True)