from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
import pymongo
from twilio.rest import Client 

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["wapoc"]
Rececol = mydb["WaMsg"] 
Replcol = mydb["WaReplys"] 
Sentcol = mydb["WaSent"]
account_sid = 'AC671789b6e19da8927007570572dfafef' 
auth_token = '2efe68e44e889eeecfb0c8760c3778d0' 
_from = 'whatsapp:+14155238886'
_body = 'Hello! This is an editable text message. You can edit it and send it to your friends.'
_to = 'whatsapp:+918297388291'




@app.route("/getall", methods=['GET'])
def wa_getall():
   all_msgs =  Rececol.find({},{"_id":0}).sort("_id",-1).limit(2)
   list_cur = list(all_msgs)
   json_data = json.dumps(list_cur)
   return json_data

@app.route("/reply", methods=['POST'])
def wa_reply():
    req_data = request.form.to_dict()
    clnt = Client(account_sid, auth_token) 
    message = clnt.messages.create(from_=_from,body=_body,to=_to)
    dct = message.__dict__
    print(type(dct['_properties']))
   #  for key, value in dct.items():
   #    print("------------------")
   #    print(key)
   #    print("------------------")
   #    print(value)
    #Sentcol.insert_one(dct)
    #Replcol.insert_one(req_data)
    return "ok"


@app.route("/receipt", methods=['POST'])
def wa_receipt():

   wa_msg = request.form.to_dict()
    
   #print(wa_msg)
    
   Rececol.insert_one(wa_msg)
   #checking if media exist needs to handle accordingly

   hasmedia = wa_msg['NumMedia']
   if hasmedia == '1':

      try: # Storing the file that user send to the Twilio whatsapp number in our computer
         msg_url=wa_msg['MediaUrl0']  # Getting the URL of the file
         print("msg_url-->",msg_url)
         msg_ext=wa_msg['MediaContentType0']  # Getting the extension for the file
         print("msg_ext-->",msg_ext)
         ext = msg_ext.split('/')[-1]
         print("ext-->",ext)
         if msg_url != None:
            json_path = requests.get(msg_url)
            filename = msg_url.split('/')[-1]
            open(filename+"."+ext, 'wb').write(json_path.content)  # Storing the file
      except:
            print("no url-->>")   
            print("Media Not found")

   #lets extract the message and figure out how to handle it
   msg = wa_msg['Body'].lower()  # Converting the message to lower case
   resp = MessagingResponse()
   reply=resp.message()
   
   #call handler to handle the message

   # Text response
   
   if msg == "hi":
      reply.body("hello! I am just a bot")

   # Image response
   elif msg == "image":
      #reply.media('gateway-india-mumbai-gateway.jpg',caption="Gateway of India")
      reply.body("Image sent")
   # Audio response
   elif msg == "audio":
      reply.media('http://www.largesound.com/ashborytour/sound/brobob.mp3')
        
   # Video response
   elif msg == "video":
      #reply.media('https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4')
      reply.body("Video sent")
    
   # Document response
   elif msg == "file":
      reply.media('https://lienzo.s3.amazonaws.com/images/8d543af756864231e8bfa6532a230bd5-in-invoice-template-PDF-2.pdf')
      reply.body("Your Invoice attached")
    
   else:
      strng = "Hi " + wa_msg['ProfileName'] + " you said '--" + wa_msg['Body'] + "--'"
      reply.body(strng)
      print(reply.media)

   return str(resp)

if __name__ == "__main__":
    app.run(debug=True)