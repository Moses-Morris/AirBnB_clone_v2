#!/usr/bin/python3
"""
Flask web application
Web Application should be listening at 0.0.0.0 to allow other users on the network
to discover and access the application on port 5000
Routes: '/' (Default entry index of App)
Route Option : strict_slashes=False
"""

from flask import Flask

"""Instance of Flask App"""
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
	return "Hello HBNB!"

if __name__ == "__main__":
	app.run(host="0.0.0.0")
