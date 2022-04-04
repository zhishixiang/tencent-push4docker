from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>dd</p>"
@app.route("/asd")
def hello_world1():
    return "666"