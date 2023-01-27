from datetime import datetime
import asyncio
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
from json import JSONEncoder
from twilio.rest import Client 
import dataaccess as da


app = Flask(__name__)

account_sid = 'AC671789b6e19da8927007570572dfafef' 
auth_token = '8fff8d7723c370c49ac11912f53a550b'
_from = 'whatsapp:+14155238886'
_body = 'Unable to send message from System'
_to = 'whatsapp:+919821335868'


@app.route("/api/getall", methods=['GET'])
def wa_getall():
   json_data = asyncio.run(da.Getallchats())
   return json_data

@app.route("/api/gethistory", methods=['POST'])
def wa_gethistory():
   req_data = request.form.to_dict()
   mobileno = req_data['MobileNo']
   json_data = asyncio.run(da.Getchat(mobileno))

   return json_data


@app.route("/api/reply", methods=['POST'])
def wa_reply():
   req_data = request.form.to_dict()
   _body = req_data['ReplyMsg']
   _to = req_data['SentTo']
   _from = req_data['SentFrom']
   clnt = Client(account_sid, auth_token) 
   message = clnt.messages.create(from_=_from,body=_body,to=_to)
   recd = dict(message._properties)
   asyncio.run(da.insertReply(recd))
   return "ok"

@app.route("/api/receipt", methods=['POST'])
def wa_receipt():

   wa_msg = request.form.to_dict()
   asyncio.run(da.insertReceived(wa_msg))
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
            print("Media Not found")

   #lets extract the message and figure out how to handle it
   msg = wa_msg['Body'].lower()  # Converting the message to lower case
   resp = MessagingResponse()
   reply=resp.message()
   
   list_greet = ['hi','hello','hey']
   list_image = ['image','pic','picture']
   list_audio = ['audio','song']
   list_video = ['video','movie']
   list_file = ['invoice','inv','invoices','challan','challans','bill','bills']
   list_info = ['infomation','information','info','help']
   
   if (msg in list_greet ):
      strng = "Hi " + wa_msg['ProfileName'] + " : I am just a bot " 
      reply.body(strng)

   # Image response
   elif (msg in list_image):
      #reply.media('gateway-india-mumbai-gateway.jpg',caption="Gateway of India")
      reply.body("Image sent")
   
   # Audio response
   elif (msg in list_audio):
      reply.media('http://www.largesound.com/ashborytour/sound/brobob.mp3')
        
   # Video response
   elif (msg in list_video):
      reply.media('https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4')
      reply.body("Video sent")
    
   # Document response
   elif (msg in list_file):
      reply.media('https://lienzo.s3.amazonaws.com/images/8d543af756864231e8bfa6532a230bd5-in-invoice-template-PDF-2.pdf')
      reply.body("Your Invoice attached")
    
   elif (msg in list_info):
      print("hi")

   else:
      # strng = "Hi " + wa_msg['ProfileName'] + " you said '--" + wa_msg['Body'] + "--'"
      # reply.body(strng)
      # print(reply.media)
      print('msg dumped')

   return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


