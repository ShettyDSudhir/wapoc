import asyncio
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 
import dataaccess as da
from flask_cors import CORS
import re
import gtpchat

app = Flask(__name__)
CORS(app)

account_sid = 'AC671789b6e19da8927007570572dfafef' 
auth_token = 'fefd54ebcbfaa246a738d00848c5ad17'
_from = 'whatsapp:+14155238886'
_body = 'Unable to send message from System'
_to = 'whatsapp:+919821335868'

@app.route("/api/dashboard1", methods=['GET'])
def wa_dashboard1():
   json_data = asyncio.run(da.getdashboard1())
   return json_data

@app.route("/api/sent", methods=['GET'])
def wa_getallsent():
   json_data = asyncio.run(da.getallsent())
   return json_data

@app.route("/api/recd", methods=['GET'])
def wa_getallrec():
   json_data = asyncio.run(da.getallreceived())
   return json_data

@app.route("/api/chat", methods=['GET'])
def wa_getallchat():
   json_data = asyncio.run(da.getallchats())
   return json_data

@app.route("/api/history", methods=['GET'])
def wa_gethistory():
   req_data = request.args.to_dict()
   #print(req_data)
   mobileno = req_data["MobileNo"]
   #print(mobileno)
   json_data = asyncio.run(da.getchat(mobileno))

   return json_data

@app.route("/api/reply", methods=['GET'])
def wa_reply():
   req_data = request.args.to_dict()
   _body = req_data['ReplyMsg']
   _to = "whatsapp:+91" + req_data['SentTo']
   print(_body)
   print(_to)
   clnt = Client(account_sid, auth_token) 
   message = clnt.messages.create(from_=_from,body=_body,to=_to)
   recd = dict(message._properties)
   asyncio.run(da.insertreply(recd))
   return "Message Sent"

@app.route("/api/receipt", methods=['POST'])
def wa_receipt():

   wa_msg = request.form.to_dict()
   asyncio.run(da.insertreceived(wa_msg))
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
   list_order = ['order','orders']
   list_audio = ['audio','song','recording']
   list_video = ['video','movie']
   list_file = ['invoice','inv','invoices','challan','challans','bill','bills']
   list_info = ['infomation','informations','info','help']
   

   if any(word.lower() in msg.lower() for word in list_greet):
      strng = "Hi " + wa_msg['ProfileName'] + " : I am just a bot " 
      reply.body(strng)

   # Image response
   elif any(word.lower() in msg.lower() for word in list_image):
      #reply.media('gateway-india-mumbai-gateway.jpg',caption="Gateway of India")
      reply.body("Image sent")

   # Order response
   elif any(word.lower() in msg.lower() for word in list_order):
      num = re.findall(r'\d+', msg)
      for invs in num:
         retval = da.findorder(invs)
         reply.body(retval)
   
   # Audio response
   elif any(word.lower() in msg.lower() for word in list_audio):
      reply.media('http://www.largesound.com/ashborytour/sound/brobob.mp3')
        
   # Video response
   elif any(word.lower() in msg.lower() for word in list_video):
      reply.media('https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4')
      reply.body("Video sent")
    
   # Document response
   elif any(word.lower() in msg.lower() for word in list_file):
      reply.media('https://lienzo.s3.amazonaws.com/images/8d543af756864231e8bfa6532a230bd5-in-invoice-template-PDF-2.pdf')
      reply.body("Your document attached")
    
   elif any(word.lower() in msg.lower() for word in list_info):
      print("Implement help text here")

   elif msg[0] == '?':
      reply.body(gtpchat.getanswer(msg[1:]))


   else:
      print('msg dumped')

   return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


