import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["wapoc"]
History = mydb["ChatHistory"]

Histdict = {}


Histdict['MobileNo'] = "9821335868"
Histdict['Name'] = "Test - 04"
Histdict['Msg'] = "Hello"
Histdict['MsgType'] = "text"
Histdict['InsertedOn'] = datetime.now()
Histdict['SentRecd']  = "0"

History.insert_one(Histdict)
