import re
import sqlite3

def extractmsg(bodytext):
    xtext = num = re.findall(r'\d+', bodytext) 
    return xtext

def insertsqlite(xtext):

    conn = sqlite3.connect('wapoc.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Media(
                id INTEGER PRIMARY KEY, title TEXT, 
                type TEXT,  genre TEXT,
                onchapter INTEGER,  chapters INTEGER,
                status TEXT
                )''')
    c.execute("INSERT INTO test VALUES (?)", (xtext,))
    conn.commit()
    conn.close()

        """ for key in Fetch_msg.keys():
        print(key)
        print("Value of key->",Fetch_msg[key])
     """

def storemedia():

    try: # Storing the file that user send to the Twilio whatsapp number in our computer
        msg_url=request.form.get('MediaUrl0')  # Getting the URL of the file
        #print("msg_url-->",msg_url)
        msg_ext=request.form.get('MediaContentType0')  # Getting the extension for the file
        #print("msg_ext-->",msg_ext)
        ext = msg_ext.split('/')[-1]
        #print("ext-->",ext)
        if msg_url != None:
            json_path = requests.get(msg_url)
            filename = msg_url.split('/')[-1]
            open(filename+"."+ext, 'wb').write(json_path.content)  # Storing the file
    except:
        print("no url-->>")
 