from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse



app = Flask(__name__)



@app.route("/wasms", methods=['POST'])
def wa_sms_reply():

    wa_msg = request.form.to_dict()
    
    #print(wa_msg)
    #checking if media exist needs to handle accordingly

    hasmedia = wa_msg['NumMedia']
    if hasmedia == '1':
        print("Media found")
        print(wa_msg['MediaUrl0'])
        print(wa_msg['MediaContentType0'])

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
        strng = "Hi " + wa_msg['ProfileName'] + " you said '-" + wa_msg['Body'] + "-'"
        reply.body(strng)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)