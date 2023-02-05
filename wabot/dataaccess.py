import pymongo
import json
import asyncio
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["wapoc"]
Rececol = mydb["WaReceived"] 
Replcol = mydb["WaReplys"] 
Histcol = mydb["ChatHistory"]
custcol = mydb["customers"]
ordercol = mydb["orders"]

async def insertreply(data):
    
    data['sent_date'] = datetime.now()
    Replcol.insert_one(data)
    chatdata = {}
    chatdata['MobileNo'] = data['to']
    chatdata['Name'] = 'N.A.'
    chatdata['Msg'] = data['body']
    chatdata['MsgType'] = data["num_segments"]
    chatdata['InsertedOn'] = data['sent_date']
    chatdata['SentRecd']  = "1"
    Histcol.insert_one(chatdata)
   
async def insertreceived(data):
    hasmedia = data['NumMedia']
    chatdata = {}
    data['rec_date'] = datetime.now()
    Rececol.insert_one(data)
    chatdata['MobileNo'] = data['From']
    chatdata['Name'] = data['ProfileName']
    chatdata['Msg'] = data['Body']
    chatdata['MsgType'] = data["NumMedia"]
    chatdata['InsertedOn'] = data['rec_date']
    chatdata['SentRecd']  = "0"
    if hasmedia == '1':
        chatdata["MediaUrl"] = data["MediaUrl0"]
    else:
        chatdata["MediaUrl"] = "N.A."

    Histcol.insert_one(chatdata)

async def getchat(mobileno):
    _mobile = "whatsapp:+91" + mobileno
    all_msgs =  Histcol.find({"MobileNo" : _mobile},{"_id":0}).sort("InsertedOn",1).limit(50)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def getcllchats():
    all_msgs =  Histcol.find({},{"_id":0}).sort("InsertedOn",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def getallsent():
    all_msgs =  Replcol.find({},{"_id":0}).sort("sent_date",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def getallreceived():
    all_msgs =  Rececol.find({},{"_id":0}).sort("rec_date",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def getdashboard1():
    all_msgs =  custcol.find({},{"_id":0}).sort("customers",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

def inserthistory(data):
    data['InsertedOn'] = datetime.now()
    Histcol.insert_one(data)

def findorder(orderid):
    list_cur =  ordercol.find_one({"orderno" : orderid})

    if(len(list_cur) == 0):
        retstr = 'No order found for order id : ' + orderid
    else:
        retstr = 'order-No :' + list_cur['orderno'] + '\n' + 'patient name : ' + list_cur['patient'] + '\n' + 'Status :' + list_cur['status'] + '\n' + "ETA : " + list_cur['ETA']

    return retstr

