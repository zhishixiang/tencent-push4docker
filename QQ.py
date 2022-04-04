import json
from tokenize import group
from flask import Flask,request,jsonify
import json
app = Flask(__name__)

@app.route("/",methods=['POST'])
def recvMsg():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data["post_type"] == "meta_event":
        if json_data["meta_event_type"] == "heartbeat":
            print("接收心跳信号成功")
    return "<p>dd</p>"
    