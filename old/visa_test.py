## TWILIO CODE Q6uW12JvrICOSkVwx-oLcjpiypKKaWWabHD1UH6S





# # cookies      = json.dumps( session.cookies.get_dict() ,indent=4) # convert cookies to json
# # cookies = json.loads( getDataFromFile("cookies.json") )
# from pprint import pprint
# import json
# from datetime import datetime

# """
# ############## JSON #######################
# # loads - convert string to json (dict)   #
# # dumps - convert json(dict) to string    #
# ###########################################

# """

# def writeDataToFile(file,text):
#     with open(file, "w") as file:
#         file.write(text)

# def getDataFromFile(file):
#     with open(file, "r") as file:
#         text = file.read()
#     return text

# d = json.loads( getDataFromFile("test.json") )
# d["age"] = 100
# d["name"] = "Dzmitry"
# d["cookiesModifed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# pprint(d)
# print(type(d))

# writeDataToFile("test.json", json.dumps(d, indent=4))

# from twilio.rest import Client
# import json 
# from pprint import pprint

# SRC     = "sourse.json"

# def getDataFromFile(file):
#     with open(file, "r") as file:
#         text = file.read()
#     return text

# NOTIF = "NOTIF"
# CURSIVE = ""
# END = ""
# def sendNotification(src):
    # text = src.get('notificationText',"ERRO No Text in response")

    # print(f"{NOTIF} I'm gonna send notification with text :\n\t{CURSIVE}{text}{END}")
    # # Your Account SID , TOKEN , NUMBER FROM SEND from twilio.com/console
    # SID         = "AC4b1fb84e16c1460ad115de4d3cc51675"
    # TOKEN       = "69f6bb64973adb4609485192c84c61ab"
    # NUMBER_FROM = "+14172323445"
    # NUMBERS_TO  = ["+375293327812"]#,"+375447335300","375447335301"] 
    
    # client = Client(SID,TOKEN)
    # for number in NUMBERS_TO:
    #     message = client.messages.create(to=number,from_="+14172323445",body="text")
    #     print(f"{NOTIF} {SUCCESS} Sending Notification to {number}")
    #     # print(message)

    # print(f"{NOTIF} {SUCCESS} SMS notification was sent ")

    # we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC4b1fb84e16c1460ad115de4d3cc51675", "c07a9c1cc4df8b0b92906e32c4134f62")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
msg = client.messages.create(to="+375293327812", 
                    from_="+14172323445", 
                    body="Hello from Python!")


print(msg.body)
# src = json.loads(getDataFromFile(SRC))
# # pprint(src)
# sendNotification(src)