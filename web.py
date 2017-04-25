from flask import Flask, jsonify, render_template, url_for
from tapperWeb import getTapperData
app = Flask(__name__)

@app.route("/list/<location>")
def home(location):
    return render_template("beer-list.html", location=location)

@app.route("/api/v1/beers/<location>", methods=['GET'])
def beers(location):
    return jsonify({'data': render_template('beer-element.html', beerList=getTapperData(location))})

def updateDatabase():
    print("not implemented")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)