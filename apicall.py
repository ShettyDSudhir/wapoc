# Description: This file contains the code for the API call to the Twilio API
from flask import Flask, request

from twilio.rest import Client 
 
account_sid = 'AC671789b6e19da8927007570572dfafef' 
auth_token = 'e8280996cc98539d2705bf68e969087a' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Hello! This is an editable text message. You are free to change it and write whatever you like.',      
                              to='whatsapp:+919821335868' 
                          ) 
 
print(message.sid)