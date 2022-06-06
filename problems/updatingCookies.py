'''

PROBLEM [SOLVED]: WE want our cookies be updated every 30 minutes (1800 seconds)

'''

from datetime import datetime  , timedelta
import pytz 

SRC =  {
    "refreshDate":"2022:06:05-10:41:52(+0300)", # cookies should be modifeded
    "modifiedDate":"2022:06:05-10:45:37(+0300)", # cokies where modifed
    "refreshEvery":1800, # seconds
}

timeFormat = "%Y:%m:%d-%H:%M:%S(%z)"#"%Y-%m-%d_%H:%M:%S_%z",

"""
==============VERSION 1================
we have in our src file date when we need to update cookies (now(in the past)+refreshEvery)
if this date is less than now, we don't do anything
but if this date bigger than current date, we update cookies

"""
mD = datetime.strptime(SRC["modifiedDate"],timeFormat)
rD = datetime.strptime(SRC["refreshDate"],timeFormat)

# check if cookies are older than refresh them
if datetime.now(pytz.timezone("Europe/Moscow"))  > datetime.strptime(SRC["refreshDate"],timeFormat):
    print("cookies are older than refresh them")
    SRC["modifiedDate"] = datetime.now(pytz.timezone("Europe/Moscow")).strftime(timeFormat)
    SRC["refreshDate"]  = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(seconds=SRC["refreshEvery"])



"""
==============VERSION 2================
we have in our src file amount of second to wait before update cookies
we get last time we updated cookies 
than we look for delta between now and last time we updated cookies
if delta is bigger than refreshEvery, we refresh cookies

"""
delta = (datetime.now(pytz.timezone("Europe/Moscow")) - datetime.strptime(SRC["modifiedDate"],timeFormat) )

if delta.total_seconds() > SRC["refreshEvery"]:
    print("should refresh")
    SRC["modifiedDate"] = datetime.now(pytz.timezone("Europe/Moscow")).strftime(timeFormat)
#=================================