# Description: This file contains the code for the API call to the Twilio API
from flask import Flask, request

from twilio.rest import Client 
 
account_sid = '' 
auth_token = '' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Hello! This is an editable text message. You are free to change it and write whatever you like.',      
                              to='whatsapp:+919821335868' 
                          ) 
 
print(message.sid)

import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Set the model and prompt
model_engine = "text-davinci-003"
prompt = "Write a blog on ChatGPT"

# Set the maximum number of tokens to generate in the response
max_tokens = 1024

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Print the response
print(completion.choices[0].text)