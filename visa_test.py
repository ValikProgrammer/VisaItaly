# cookies      = json.dumps( session.cookies.get_dict() ,indent=4) # convert cookies to json
# cookies = json.loads( getDataFromFile("cookies.json") )
from pprint import pprint
import json
from datetime import datetime

"""
############## JSON #######################
# loads - convert string to json (dict)   #
# dumps - convert json(dict) to string    #
###########################################

"""

def writeDataToFile(file,text):
    with open(file, "w") as file:
        file.write(text)

def getDataFromFile(file):
    with open(file, "r") as file:
        text = file.read()
    return text

d = json.loads( getDataFromFile("test.json") )
d["age"] = 100
d["name"] = "Dzmitry"
d["cookiesModifed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
pprint(d)
print(type(d))

writeDataToFile("test.json", json.dumps(d, indent=4))