# -*- coding: utf-8 -*-
"""
* * * * *        echo "i am working every minute! ($(date))"                  >> cronLogEveryMinute
*/10 0-1 * * *   echo "from 0-1 hour every 10 minutes script run ($(date))"   >> pythonScriptRunningTest
*/30 2-9 * * *   echo "from 2-9 hour every 30 minutes script run ($(date))"   >> pythonScriptRunningTest
*/10 10-23 * * * echo "from 10-23 hour every 10 minutes script run ($(date))" >> pythonScriptRunningTest


*/10 0-1 * * *   cd /home/valikprogrammer/VisaItaly && python3 main.py
*/30 2-9 * * *   cd /home/valikprogrammer/VisaItaly && python3 main.py
*/10 10-23 * * * cd /home/valikprogrammer/VisaItaly && python3 main.py
"""

import os, sys, json
import requests, fake_useragent
import time, pytz

from datetime import datetime
from twilio.rest import Client
# from server import keep_alive

# import logging as log

# log.basicConfig(
#     level=log.INFO,
#     format='%(asctime)s %(levelname)-8s %(funcName)-17s %(message)s',# %(funcName)-17s (17 is the length of the longest function name - send Notification)
#     datefmt="%y:%m:%d-%H:%M:%S", 
#     handlers=[
#         log.FileHandler('log.log'),
#         log.StreamHandler()
#     ],
#     'disable_existing_loggers': True,
# )

import logging as log
import logging.config
log.config.fileConfig('logging.conf', disable_existing_loggers=True)

SRC_FILE = "source.json"
SRC      = json.load(open(SRC_FILE))

def writeDataToFile(file,text):
    with open(file, "w") as file:
        file.write(text)
# def addDataToFile(file,text):
#     with open(file, "a") as file:
#         file.write(text)
# def getDataFromFile(file):
#     with open(file, "r") as file:
#         text = file.read()
#     return text

def updateCookies():
    try:
        headers  = {
                "User-Agent": fake_useragent.UserAgent().random
        }
        authData = {
                "Email": "Dzmitry_Khilko@epam.com",
                "Password": "myBelarus1"
        }

        session      = requests.Session()
        authResponse = session.post(SRC["urlAuth"], headers=headers, data=authData) # autotorize at site
        if authResponse.status_code == 200:
            # log.info(f"Auth response success : {authResponse.url}")
            SRC["cookies"]         = session.cookies.get_dict() # convert cookies to dict
            SRC["cookiesModified"] = SRC["lastRequestDate"]
            log.info("Cookies was upgraded successfully")  
        else :
            log.error(f"Auth response: ({authResponse.status_code}) {authResponse.url}") 
    except Exception as e:
        log.error(f"Can't update cookies. Error: {e}")

def getVisa():
    try:
        headers  = {
            "User-Agent": fake_useragent.UserAgent().random
        }
        session  = requests.Session()

        # check if date of cookies refreshing isn't empty 
        if SRC["cookiesModified"] == "":
            log.warning("CookiesModified date is empty. Add current date to it")
            updateCookies()
        else:
            # Check if cookies are old , if it is true, get new cookies
            delta = ( datetime.strptime(SRC["lastRequestDate"],SRC["timeFormat"]) - datetime.strptime(SRC["cookiesModified"],SRC["timeFormat"]) ).total_seconds()
            if (delta > SRC["refreshEvery"] or delta < 0 ) or SRC["cookies"] == {}:
                log.warning(f"Cookies are old or empty . Get new cookies . delta = {delta}")
                updateCookies()

        # do request to the site with cookies and headers(useragent)
        response = session.get(SRC["urlVisa"], headers=headers,cookies=SRC["cookies"])  
        log.info(f"Response: ({response.status_code}) {response.url}")
        return response.text or ("No text in response "+SRC["phase"])
    except Exception as e:
        log.error(f"Can't get visa. Error: {e}")
        return ("No text in response "+SRC["phase"]) # чтоб оно не думало что раз фразы нету в тексте то значит виза есть (на самом деле фразы в тесте нету из-за ошибки)
    

def sendNotification():
    try:
        text = (SRC.get('notificationText','ERROR No Text in response {0}')).format(SRC["lastRequestDate"])
        log.info("I'm gonna send notification")
        
        for number in SRC["phones"]:
            s = f'''
            curl -X POST https://api.twilio.com/2010-04-01/Accounts/AC931feeade6da23329e10c89608c92859/Messages.json \
            --data-urlencode "Body={text}" \
            --data-urlencode "From={SRC['numberFrom']}" \
            --data-urlencode "To={number}" \
            -u AC931feeade6da23329e10c89608c92859:acb9c31465735a78a752439c86f0d626'''
            os.system(s)

        # Version1 (working with some errors[i don,t know why])
        # client = Client(SRC["sid"],SRC["token"])
        # for number in SRC["phones"]:
        #     message = client.messages.create(to=number,from_=SRC["numberFrom"],body=text)
        #     # log.info(f"Sending Notification to {number}")
        log.info("Notification was sent successfully")
    except Exception as e:
        e = ' ; '.join( str(e).split('\n') )
        log.error(f"Can't send notification. Error: {e}")
    # log.info("Notif")
    

def main():
    try: 
        SRC["lastRequestDate"] = datetime.now(pytz.timezone(SRC["tz"])).strftime(SRC["timeFormat"])            
        response = getVisa()   # get response from website

        if SRC["phrase"] in response:
            log.warning("[VISA]: NO")
        else :
            respArr = response.splitlines()
            forbiddenS   = '<!-- Matomo Code -->'
            forbiddenLen = 429
            if (len(respArr) == forbiddenLen and respArr[5].strip() == forbiddenS.strip()):
                log.warning("[Visa] : NO (fake html page! )")
                updateCookies()
            else:
                log.critical("[VISA]: YES")
                sendNotification()
                writeDataToFile(f'html/visa{SRC["lastRequestDate"]}.html',response) # write our response to file
        writeDataToFile(SRC_FILE,json.dumps(SRC,indent=4)) # write(refresh) our SRC file
        # time.sleep(600)
        sys.exit(0)
    except KeyboardInterrupt:
        log.critical("Killed by user")
        sys.exit(0)
    except Exception as e:
        log.error(f"Failed to get visa. Error: {e}",)
        

if __name__ == "__main__":
    # keep_alive()
    main()
