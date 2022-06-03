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

PHRASE       = "Al momento non ci sono date disponibili per il servizio richiesto" # В настоящее время нет свободных дат для запрошенной услуги
COUNTER_FILE = "counter.txt"
LOG_FILE     = "log.txt"
LAST_COOKIES_UPGRADE_FILE = "lastCookiesDate.txt"

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

def getVisa():
    # try:
        urlAuth   = "https://prenotami.esteri.it/Home/Login"
        urlVisa   = "https://prenotami.esteri.it/Services/Booking/1090"
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
        if getDataFromFile(LAST_COOKIES_UPGRADE_FILE) == "":
            writeDataToFile(LAST_COOKIES_UPGRADE_FILE, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            lastCookiesDate = datetime.strptime(getDataFromFile(LAST_COOKIES_UPGRADE_FILE), "%Y-%m-%d %H:%M:%S")
            delta = datetime.now() - lastCookiesDate
            if delta.days >= 1: # we want to get new cookies every day
                authResponse = session.post(urlAuth, headers=headers, data=data) # autotorize at site
                print(f"{GV} Auth response: ({GREEN}{authResponse.status_code}{END}) {authResponse.url}")

                cookies      = json.dumps( session.cookies.get_dict() ,indent=4) # convert cookies to json

                writeDataToFile("cookies.json", cookies)
                writeDataToFile(LAST_COOKIES_UPGRADE_FILE, datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # write the date of upgrading cookies to file lastCookiesDate.txt
                print(f"{GV} {SUCCESS} Cookies was upgraded ")

        cookies = json.loads( getDataFromFile("cookies.json") )

        response = session.get(urlVisa, headers=headers,cookies=cookies)  
        print(f"{GV} {SUCCESS} Response: ({GREEN}{response.status_code}{END}) {response.url}")
        return response.text or ("No text in response "+PHRASE)
    # except:
    #     print(f"{GV} {ERROR} Can't get visa")
    


def sendNotification(text="ERRO No Text in response"):
    try:
        print(f"{NOTIF} I'm gonna send notification with text :\n\t{CURSIVE}{text}{END}")
        # Your Account SID , TOKEN , NUMBER FROM SEND from twilio.com/console
        SID         = "AC4b1fb84e16c1460ad115de4d3cc51675"
        TOKEN       = "69f6bb64973adb4609485192c84c61ab"
        NUMBER_FROM = "+14172323445"
        NUMBERS_TO  = ["+375293327812"]#,"+375447335300","375447335301"] 
        
        client = Client(SID,TOKEN)
        for number in NUMBERS_TO:
            message = client.messages.create(to=number,from_=NUMBER_FROM,body=text)
            print(f"{NOTIF} {SUCCESS} Sending Notification to {number}")
            print(message)

        print(f"{NOTIF} {SUCCESS} SMS notification was sent ")
    except:
        print(f"{NOTIF} {ERROR}  Can't send notification")
    

def main():
    amountOfStarting = 0
    while True:
        amountOfStarting+=1
        try:
            print(f"\n{MAIN} Starting {ORANGE}{amountOfStarting}{END} time")
            text = getVisa()                            # get response from website

            if PHRASE in text:
                print(f"[VISA]: {RED}NO{END}")
                time.sleep(300)
            else :
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get current date and time
                addDataToFile(LOG_FILE,"\n"+str(now)) # add current date and time to log file
                print(f"[VISA]: {GREEN}YES{END} {ORANGE}(now = {now}){END} !")

                notificationText = f"""Urgently!\n  Visa is available now!\n  Go to the https://prenotami.esteri.it/Services/Booking/1090\n\t{now}"""
                sendNotification(notificationText)

                counter = int(getDataFromFile(COUNTER_FILE))     # get counter
                writeDataToFile(f"html/visa{counter}.html",text) # write our response to file
                writeDataToFile(COUNTER_FILE,str(counter+1))     # increase counter
                time.sleep(60)

        except KeyboardInterrupt:
            print (f'\n{ORANGE}Killed by user{END}')
            sys.exit(0)
        except ValueError:
            print(f"{MAIN} {ERROR} Can't convert to int (Counter file is empty. Add 0 to it)")
            writeDataToFile(COUNTER_FILE,"0")
            time.sleep(600)
        except:
            print(f"{MAIN} {ERROR} Faild to get visa. Unknown error.")
            time.sleep(600)
        

if __name__ == "__main__":
    main()
