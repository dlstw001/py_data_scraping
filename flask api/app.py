from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "<p>Hello, World!</p>"

@app.route("/getlink")
def getlink():
    return "<p>Get link!</p>"