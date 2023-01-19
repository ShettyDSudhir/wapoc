import re

def extractmsg(bodytext):
    xtext = num = re.findall(r'\d+', bodytext) 
    return xtext
