from globals import tappedLocations, locations
from tapperWeb import getTapperData
from bottleOpenerWeb import getBottleOpenerData
from pymongo import MongoClient
import sys, time

client = MongoClient()
db = client.hopcat

updateTime = 86400.0 # 1 Day

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
			if location not in tappedLocations:
				tappedLocations.append(location)
		except:
			print("Error getting Tapper data for {}: {}".format(location, sys.exc_info()[0]))
			if location in tappedLocations:
				tappedLocations.remove(location)

def updateLoop():
	startTime = time.time()
	while True:
		updateDatabase()
		time.sleep(updateTime - ((time.time() - startTime) % 60.0))