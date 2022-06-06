# -*- coding: utf-8 -*-
import os, sys, json
import requests, fake_useragent
import time, pytz

from datetime import datetime
from twilio.rest import Client
from server import keep_alive

import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(levelname)-8s %(funcName)-17s %(message)s',# %(funcName)-17s (17 is the length of the longest function name - send Notification)
    datefmt="%y:%m:%d-%H:%M:%S", 
    handlers=[
        # logging.FileHandler('logging.log'),
        logging.StreamHandler()
    ]
)
# RED     = "\033[31m"
# GREEN   = "\033[32m"
# ORANGE  = "\033[33m"
# BLUE    = "\033[34m"
# CURSIVE = "\033[3m"
# END     = "\033[0m"

# MAIN    = "[{BLUE}MAIN{END}]"
# MAIN = "MAIN"
# GV      = "[{BLUE}GV{END}]"
# NOTIF   = "[{BLUE}NOTIF{END}]"
# UK      = "[{BLUE}UK{END}]"

# ERROR   = "|{RED}ERROR{END}|"
# WARNING = "|{ORANGE}WARNING{END}|"
# SUCCESS = "|{GREEN}SUCCESS{END}|"

SRC_FILE     = "sourse.json"
SRC = json.load(open(SRC_FILE))

print("1")
def sendNotification():
    print("2")
    try:
        print("3")
        text = SRC.get('notificationText','ERROR No Text in response {0}').format(SRC["lastRequestDate"])
        # log.info(f"I'm gonna send notification with text : {text}")
        
        print("4")
        client = Client(SRC["sid"],SRC["token"])
        for number in SRC["phones"]:
            print("5")
            client.messages.create(to=number,from_=SRC["numberFrom"],body=text)
            print("6")
            # log.info(f"Sending Notification to {number}")

    except Exception as e:
        print("7")
        print("ERROR:",e)
        # log.error(f"Can't send notification. Error: {e}")
    # log.info("Notif")

print("8")
sendNotification()
print("9")