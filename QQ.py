from asyncio.windows_events import NULL
from email import message
import json
from tokenize import group
from flask import Flask,request,jsonify
import json
app = Flask(__name__)

def msgFormat(msg):
    if "CQ:image" in msg:
        msg = "[图片]"
    elif "CQ:record" in msg:
        msg = "[语音]"
    elif "CQ:share" in msg:
        msg = "[链接]"
    elif "CQ:music" in msg:
        msg = "[音乐分享]"
    elif "CQ:redbag" in msg:
        msg = "[红包]"
    elif "CQ:forward" in msg:
        msg = "[合并转发]"
    return msg

@app.route("/",methods=['POST'])
def recvMsg():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data["post_type"] == "meta_event":
        if json_data["meta_event_type"] == "heartbeat":
            print("接收心跳信号成功")
    elif json_data["message_type"] == "private":
        nickName = json_data["sender"]["nickname"]
        msg = json_data["message"]
        print("来自%s的私聊消息:%s"%(nickName,msg))
    elif json_data["message_type"] == "group":
        groupId = json_data["group_id"]
        nickName = json_data["sender"]["nickname"]
        msg = msgFormat(json_data["message"])
        print("来自%s的群聊消息:%s:%s"%(groupId,nickName,msg))
    return "200 OK"
    