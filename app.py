from http import server
import imp
from flask import Flask
import services
app = Flask(__name__)



@app.route("/get_all")
def get_all_links():
    services.get_all.get_all()
    return "<p>Finished</p>"

@app.route("/get_one")
def get_one_link():
    services.get_one














