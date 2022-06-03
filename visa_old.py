import os
import sys
import requests
import fake_useragent
from twilio.rest import Client
from datetime import datetime
import time
import json

COUNTER_FILE = "counter.txt"
LOG_FILE     = "log.txt"
PHRASE       = "Al momento non ci sono date disponibili per il servizio richiesto" # В настоящее время нет свободных дат для запрошенной услуги

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
        print(f"{GV} I'm gonna get visa")
        urlAuth   = "https://prenotami.esteri.it/Home/Login"
        urlVisa   = "https://prenotami.esteri.it/Services/Booking/1090"
        userAgent = fake_useragent.UserAgent().random

        headers = {
            "User-Agent": userAgent
        }
        data = {
            "Email": "Dzmitry_Khilko@epam.com",
            "Password": "myBelarus1"
        }
        # cookies = (getDataFromFile("cookies_dict2.txt"))
        # print(cookies)

        session = requests.Session()

        authResponse = session.post(urlAuth, headers=headers, data=data)#cookies=cookies

        sessionCookies = session.cookies.get_dict()
        cookies = json.loads( sessionCookies )

        # lastCookiesDateFile = "lastCookiesDate.txt"

        # if getDataFromFile(lastCookiesDateFile) == "":
        #     writeDataToFile(lastCookiesDateFile, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # else:
        #     lastCookiesDate = datetime.strptime(getDataFromFile(lastCookiesDateFile), "%Y-%m-%d %H:%M:%S")
        #     delta = datetime.now() - lastCookiesDate
        #     if delta.days >= 1:
        #         writeDataToFile(lastCookiesDateFile, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #         print("You need change cookies")

        #         authResponse = session.post(urlAuth, headers=headers, data=data)#cookies=cookies
        #         print(f"{GV} Auth response: ({GREEN}{authResponse.status_code}{END}) {authResponse.url}")

        #         sessionCookies = session.cookies.get_dict()
        #         cookies = json.dumps(sessionCookies,indent=4)
        #         writeDataToFile("cookies.json", cookies)
        #     else:# just get cookies fom json file
        #         print("helloword")
        # cookies =  json.loads( getDataFromFile("cookies.json") )

        response = session.get(urlVisa, headers=headers,cookies=cookies)  

    # #### COOKIES
    #     # cookies = [
    #     #     for key in session.cookies 
    #     # # ]
    #     cookies = session.cookies
    #     writeDataToFile("cookies.txt", str(cookies))
    #     writeDataToFile("cookies_dict2.txt", str(cookies.get_dict() ))
    #     """ === about redirects ===
    #     if response.history:
    #         print(f"{GV} {ORANGE}Request was redirected.{END} HISTORY:")
    #         for resp in response.history:
    #             print(f"\t({GREEN}{resp.status_code}{END}) {resp.url}")
    #         # print(f"{GV} Final destination: ({GREEN}{response.status_code}{END}) {response.url}")
    #     """
        print(f"{GV} {SUCCESS} Response: ({GREEN}{response.status_code}{END}) {response.url}")
        return response.text or "No text in response"+PHRASE
    # except:
    #     print(f"{GV} {ERROR} Can't get visa")
    


def sendNotification(text="[ERROR] NO TEXT in Notification"):
    try:
        print(f"{NOTIF} I'm gonna send notification with text :\n\t{CURSIVE}{text}{END}")

        # client = Client("AC4b1fb84e16c1460ad115de4d3cc51675", "69f6bb64973adb4609485192c84c61ab")
        # client.messages.create(to="+375293327812", from_="+14172323445", body=text)

        print(f"{NOTIF} {SUCCESS} SMS notification was sent SUCCESSFULLY")
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
                counter = int(getDataFromFile(COUNTER_FILE))     # get counter
                writeDataToFile(f"html/visa{counter}.html",text) # write our response to file
                writeDataToFile(COUNTER_FILE,str(counter+1))     # increase counter

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get current date and time
                txt = f""" Urgent
                Visa is available now!
                    {now}"""
                print(f"[VISA]: {GREEN}YES{END} {ORANGE}(now = {now}){END} !")

                addDataToFile(LOG_FILE,"\n"+str(now)) # add current date and time to log file
                sendNotification(txt)
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
