from http import server
import imp
from flask import Flask
from services import getAll

app = Flask(__name__)



@app.route("/get_all")
def get_all_links():
    getAll.get_all()
    return "<p>Finished</p>"
















