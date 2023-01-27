import pymongo
import json
import asyncio
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["wapoc"]
Rececol = mydb["WaReceived"] 
Replcol = mydb["WaReplys"] 
Histcol = mydb["ChatHistory"]

async def insertReply(data):
    
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

   
async def insertReceived(data):
    
    data['rec_date'] = datetime.now()
    Rececol.insert_one(data)
    chatdata = {}
    chatdata['MobileNo'] = data['From']
    chatdata['Name'] = data['ProfileName']
    chatdata['Msg'] = data['Body']
    chatdata['MsgType'] = data["NumMedia"]
    chatdata['InsertedOn'] = data['rec_date']
    chatdata['SentRecd']  = "0"
    Histcol.insert_one(chatdata)


async def Getchat(mobileno):
    all_msgs =  Histcol.find({"MobileNo" : mobileno},{"InsertedOn":0}).sort("_id",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def Getallchats():
    all_msgs =  Histcol.find({},{"_id":0}).sort("InsertedOn",-1).limit(2)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def GetallSent():
    all_msgs =  Replcol.find({},{"_id":0}).sort("sent_date",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data

async def GetallReceived():
    all_msgs =  Rececol.find({},{"_id":0}).sort("rec_date",-1).limit(20)
    list_cur = list(all_msgs)
    json_data = json.dumps(list_cur, default=str)
    return json_data


def insertHistory(data):
    data['InsertedOn'] = datetime.now()
    Histcol.insert_one(data)