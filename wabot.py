from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

@app.route("/wa")
def wa_hello():
    return "Hello, World!"

@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    Fetch_msg= request.form.to_dict()
    #json_data = json.dumps(Fetch_msg, indent = 4) 
    #print(json_data)
    for key in Fetch_msg.keys():
        print(key)
        print("Value of key->",Fetch_msg[key])


    try: # Storing the file that user send to the Twilio whatsapp number in our computer
        msg_url=request.form.get('MediaUrl0')  # Getting the URL of the file
        print("msg_url-->",msg_url)
        msg_ext=request.form.get('MediaContentType0')  # Getting the extension for the file
        print("msg_ext-->",msg_ext)
        ext = msg_ext.split('/')[-1]
        print("ext-->",ext)
        if msg_url != None:
            json_path = requests.get(msg_url)
            filename = msg_url.split('/')[-1]
            open(filename+"."+ext, 'wb').write(json_path.content)  # Storing the file
    except:
        print("no url-->>")

    msg = request.form.get('Body').lower()  # Reading the message from the whatsapp
    print("msg-->",msg)
    resp = MessagingResponse()
    reply=resp.message()
    # Create reply

    # Text response
    if msg == "hi":
       reply.body("hello! I am a bot")

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
    
    else:
        reply.body("to get order details send msg in the below format\n, Job id: xxxxxxxx")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)