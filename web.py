from flask import Flask, jsonify, render_template
from tapperWeb import getTapperData
app = Flask(__name__)

@app.route("/list/<location>")
def home(location):
    return render_template("beer-list.html", location=location)

@app.route("/api/v1/beers/<location>", methods=['GET'])
def beers(location):
    return jsonify(getTapperData(location))

if __name__ == "__main__":
    app.run(debug=True)