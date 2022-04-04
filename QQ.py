from asyncio.windows_events import NULL
from email import message
import json
from tokenize import group
from flask import Flask,request,jsonify
import json
import requests


with open("config.json","r",encoding = 'UTF-8') as f:
    config = json.load(f)
group_whitelist = config["WhiteList"]

groupInfo = json.loads(requests.get("http://localhost:5700/get_group_list").text)
userId = json.loads(requests.get("http://localhost:5700/get_login_info").text)["data"]["user_id"]

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
    elif "戳一戳" in msg:
        msg = "戳了你一下"
    return msg

def getGroupName(groupId):
    length = len(groupInfo["data"])
    for i in range(length):
        if groupId == groupInfo["data"][i]["group_id"]:
            return groupInfo["data"][i]["group_name"]

@app.route("/",methods=['POST'])
def recvMsg():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data["post_type"] == "meta_event":
        if json_data["meta_event_type"] == "heartbeat":
            print("接收心跳信号成功")
    elif json_data["message_type"] == "private":
        nickName = json_data["sender"]["nickname"]
        msg = msgFormat(json_data["message"])
        print("来自%s的私聊消息:%s"%(nickName,msg))
    elif json_data["message_type"] == "group":
        groupId = json_data["group_id"]
        groupName = getGroupName(groupId)
        nickName = json_data["sender"]["nickname"]
        msg = msgFormat(json_data["message"])
        if groupId in group_whitelist:
            print("群聊%s的消息:%s:%s"%(groupName,nickName,msg))
        elif "[CQ:at,qq=%s]"%userId in msg:
            msg = msg.replace("[CQ:at,qq=%s]"%userId,"[有人@我]")
            print("群聊%s有人@我:%s:%s"%(groupName,nickName,msg))
    return "200 OK"
    