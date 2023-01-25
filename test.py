from twilio.rest import Client 
 
account_sid = 'AC671789b6e19da8927007570572dfafef' 
auth_token = '2efe68e44e889eeecfb0c8760c3778d0' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Hi Sudhir This is an demo msg. You asked for support help.',      
                              to='whatsapp:+918297388291' 
                          ) 
 
print(message)