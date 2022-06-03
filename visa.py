import os
import sys
import requests
import fake_useragent
from twilio.rest import Client
from datetime import datetime
import time
import json

RED     = "\033[31m"
GREEN   = "\033[32m"
ORANGE  = "\033[33m"
BLUE    = "\033[34m"
CURSIVE = "\033[3m"
END     = "\033[0m"

MAIN    = f"[{BLUE}MAIN{END}]"
GV      = f"[{BLUE}GV{END}]"
NOTIF   = f"[{BLUE}NOTIF{END}]"
ERROR   = f"|{RED}ERROR{END}|"
SUCCESS = f"|{GREEN}SUCCESS{END}|"

SRC     = "sourse.json"

# PHRASE       = "Al momento non ci sono date disponibili per il servizio richiesto" # В настоящее время нет свободных дат для запрошенной услуги
# COUNTER_FILE = "counter.txt"
# LOG_FILE     = "log.txt"
# LAST_COOKIES_UPGRADE_FILE = "lastCookiesDate.txt"

def writeDataToFile(file,text):
    with open(file, "w") as file:
        file.write(text)
def addDataToFile(file,text):
    with open(file, "a") as file:
        file.write(text)
def getDataFromFile(file):
    with open(file, "r") as file:
        text = file.read()
    return text

def getVisa(src):
    try:
        userAgent = fake_useragent.UserAgent().random

        headers  = {
            "User-Agent": userAgent
        }
        data     = {
            "Email": "Dzmitry_Khilko@epam.com",
            "Password": "myBelarus1"
        }

        session  = requests.Session()

        # Check if cookies are old , if it is true, get new cookies
        if src["cookiesModified"] == "":
            print(f"{GV} cookiesModified date is empty. Add current date to it")
            src["cookiesModified"] =  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
        cookiesModified = datetime.strptime(src["cookiesModified"], "%Y-%m-%d %H:%M:%S")
        delta = datetime.now() - cookiesModified
        if delta.days >= 1 or src["cookies"] == {}: # we want to get new cookies every day
            authResponse = session.post(src["urlAuth"], headers=headers, data=data) # autotorize at site
            print(f"{GV} Auth response: ({GREEN}{authResponse.status_code}{END}) {authResponse.url}")

            # cookies      = json.dumps( session.cookies.get_dict() ,indent=4) # convert cookies to json
            # src["cookies"] = cookies
            # src["cookiesModified"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # write the date of upgrading cookies 
            # print(f"{GV} {SUCCESS} Cookies was upgraded ")
            
            src["cookies"]         = session.cookies.get_dict() # convert cookies to dict
            src["cookiesModified"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # write the date of upgrading cookies 
            print(f"{GV} {SUCCESS} Cookies was upgraded ")

        response = session.get(src["urlVisa"], headers=headers,cookies=src["cookies"])  
        print(f"{GV} {SUCCESS} Response: ({GREEN}{response.status_code}{END}) {response.url}")
        return response.text or ("No text in response "+PHRASE)
    except:
        print(f"{GV} {ERROR} Can't get visa")
    


def sendNotification(src):
    try:
        text = src.get('notificationText',"ERRO No Text in response \n\t\t{0}").format(src["lastRequestDate"])

        print(f"{NOTIF} I'm gonna send notification with text :\n\t{CURSIVE}{text}{END}")
        
        client = Client(src["sid"],src["token"])
        for number in src["phones"]:
            message = client.messages.create(to=number,from_=src["numberFrom"],body=text)
            print(f"{NOTIF} {SUCCESS} Sending Notification to {number}")

    except:
        print(f"{NOTIF} {ERROR}  Can't send notification")
    

def main():
    amountOfStarting = 0
    while True:
        try:
            amountOfStarting+=1
            print(f"\n{MAIN} Starting {ORANGE}{amountOfStarting}{END} time")

            src = json.loads(getDataFromFile(SRC))
            src["lastRequestDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = getVisa(src)   # get response from website

            if src["phrase"] in response:
                print(f"[VISA]: {RED}NO{END}")
            else :
                now =  datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get current date and time
                src['log'].append(str(now)) # add current date and time to log file
                print(f"[VISA]: {GREEN}YES{END} {ORANGE}(now = {now}){END} !")

                sendNotification(src)

                counter =  src["counter"]    # get counter
                writeDataToFile(f"html/visa{counter}.html",response) # write our response to file
                src["counter"] += 1     # increase counter
            writeDataToFile(SRC,json.dumps(src,indent=4)) # write(refresh) our src to file
            time.sleep(300)
        except KeyboardInterrupt:
            print (f'\n{ORANGE}Killed by user{END}')
            sys.exit(0)
        except:
            print(f"{MAIN} {ERROR} Faild to get visa. Unknown error.")
            time.sleep(600)
        

if __name__ == "__main__":
    main()
