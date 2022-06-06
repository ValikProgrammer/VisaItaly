import os, sys, json
import requests, fake_useragent
import time , pytz

from datetime import datetime
from twilio.rest import Client
from server import keep_alive


RED     = "\033[31m"
GREEN   = "\033[32m"
ORANGE  = "\033[33m"
BLUE    = "\033[34m"
CURSIVE = "\033[3m"
END     = "\033[0m"

MAIN    = f"[{BLUE}MAIN{END}]"
GV      = f"[{BLUE}GV{END}]"
NOTIF   = f"[{BLUE}NOTIF{END}]"
UK      = f"[{BLUE}UK{END}]"

ERROR   = f"|{RED}ERROR{END}|"
WARNING = f"|{ORANGE}WARNING{END}|"
SUCCESS = f"|{GREEN}SUCCESS{END}|"

SRC_FILE     = "sourse.json"
# SRC = json.loads(getDataFromFile(SRC_FILE))
SRC = json.load(open(SRC_FILE))

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
# def getDataFromFile(file):
#     with open(file, "r") as file:
#         text = file.read()
#     return text

def updateCookies():

    headers  = {
            "User-Agent": fake_useragent.UserAgent().random
    }
    data     = {
            "Email": "Dzmitry_Khilko@epam.com",
            "Password": "myBelarus1"
    }

    session  = requests.Session()
    authResponse = session.post(SRC["urlAuth"], headers=headers, data=data) # autotorize at site
    print(f"{UK} Auth response: ({GREEN}{authResponse.status_code}{END}) {authResponse.url}")

    SRC["cookies"]         = session.cookies.get_dict() # convert cookies to dict
    SRC["cookiesModified"] = datetime.now(pytz.timezone(SRC["tz"])).strftime(SRC["timeFormat"]) # write the date of upgrading cookies 

    print(f"{UK} {SUCCESS} Cookies was upgraded ")
    SRC['log'][SRC["lastRequestDate"]].append("{UK} {SUCCESS} Cookies was upgraded ")
    

def getVisa():
    # try:
        headers  = {
            "User-Agent": fake_useragent.UserAgent().random
        }

        session  = requests.Session()

        if SRC["cookiesModified"] == "":
            print(f"{GV} {WARNING} cookiesModified date is empty. Add current date to it")
            SRC['log'][SRC["lastRequestDate"]].append("{GV} {WARNING} cookiesModified date is empty. Add current date to it")
            SRC["cookiesModified"] = SRC["lastRequestDate"]
            

            
        # cookiesModified = datetime.strptime(SRC["cookiesModified"], SRC["timeFormat"])
        # delta = datetime.now(pytz.timezone(SRC["tz"])) - cookiesModified

        # Check if cookies are old , if it is true, get new cookies
        delta = ( datetime.strptime(SRC["lastRequestDate"],SRC["timeFormat"]) - datetime.strptime(SRC["cookiesModified"],SRC["timeFormat"]) ).total_seconds()
        if (delta > SRC["refreshEvery"] or delta < 0 ) or SRC["cookies"] == {}:
            updateCookies()

        #     print("should refresh")
        # SRC["modifiedDate"] = datetime.now(pytz.timezone("Europe/Moscow")).strftime(timeFormat)

        # if (delta.days >= 1 or delta.days < 0) or SRC["cookies"] == {}: # we want to get new cookies every day
        # if SRC["counter"] >= 5:
        #     SRC["counter"] = 0
            

        response = session.get(SRC["urlVisa"], headers=headers,cookies=SRC["cookies"])  
        print(f"{GV} {SUCCESS} Response: ({GREEN}{response.status_code}{END}) {response.url}")
        SRC['log'][SRC["lastRequestDate"]].append("{GV} {SUCCESS} Response: ({GREEN}{response.status_code}{END}) {response.url}")
        return response.text or ("No text in response "+SRC["phase"])
    # except:
    #     print(f"{GV} {ERROR} Can't get visa")
    #     SRC['log'][SRC["lastRequestDate"]].append(f"{GV} {ERROR} Can't get visa")
    #     return ("No text in response "+SRC["phase"]) # чтоб оно не думало что раз фразы нету в тексте то значит виза есть (на самом деле фразы в тесте нету из-за ошибки)
    

def sendNotification():
    print(f"{NOTIF} Send notification ... ")
    # try:
    #     text = SRC.get('notificationText',"ERROR No Text in response \n{0}").format(SRC["lastRequestDate"])
    #     print(f"{NOTIF} I'm gonna send notification with text :\n\t{CURSIVE}{text}{END}")
        
    #     client = Client(SRC["sid"],SRC["token"])
    #     for number in SRC["phones"]:
    #         message = client.messages.create(to=number,from_=SRC["numberFrom"],body=text)
    #         print(f"{NOTIF} {SUCCESS} Sending Notification to {ORANGE}{number}{END}")

    # except:
    #     print(f"{NOTIF} {ERROR}  Can't send notification")
    

def main():
    amountOfStarting = 0
    while True:
        # try: 
            keep_alive()
            amountOfStarting+=1
            print(f"\n{MAIN} Starting {ORANGE}{amountOfStarting}{END} time")

            SRC["lastRequestDate"] = datetime.now(pytz.timezone(SRC["tz"])).strftime(SRC["timeFormat"])
            SRC['log'][SRC["lastRequestDate"]] = []
            
            response = getVisa()   # get response from website
            SRC["counter"] += 1     # increase counter

            if SRC["phrase"] in response:
                print(f"[VISA]: {RED}NO{END}")
                SRC['log'][SRC["lastRequestDate"]].append("{MAIN} res: NO")
            else :
                respArr = response.splitlines()

                forbiddenS   = '<!-- Matomo Code -->'
                forbiddenLen = 429
                if (len(arr) == forbiddenLen and arr[5].strip() == forbiddenS.strip()):
                    print(f"{MAIN} fake html page! \nVisa : NO")
                    updateCookies()
                    SRC['log'][SRC["lastRequestDate"]].append("{MAIN} res: NO (fake html page)")
                else:

                    # SRC['log'].append(now) # add current date and time to log file
                    print(f'[VISA]: {GREEN}YES{END} {ORANGE}(now = {SRC["lastRequestDate"]}){END} !')
                    SRC['log'][SRC["lastRequestDate"]].append("{MAIN} res: YES")
                    sendNotification()

                    # counter =  SRC["counter"]    # get counter
                    writeDataToFile(f'html/visa{SRC["lastRequestDate"]}.html',response) # write our response to file

            writeDataToFile(SRC_FILE,json.dumps(SRC,indent=4)) # write(refresh) our SRC to file
            time.sleep(300)
        # except KeyboardInterrupt:
        #     print (f'\n{ORANGE}Killed by user{END}')
        #     sys.exit(0)
        # except:
        #     print(f"{MAIN} {ERROR} Faild to get visa. Unknown error.")
        #     time.sleep(600)
        

if __name__ == "__main__":
    main()
