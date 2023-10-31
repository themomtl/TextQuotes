from cgitb import html
# from email import message
from hashlib import new
import smtplib
import email
import imaplib
import pprint
from bs4 import BeautifulSoup
import nltk
import finnhub
import time
import schedule
import pymongo
import certifi
import datetime
from finvizfinance.quote import finvizfinance
import requests
import random
import Emails
import Stocks
import MongoDB
import GroupMe


def Main():
    try:
        def WlProcesser(wl, user):
            result = ""
            for i in wl:
                db.DB(i, user).newUse()
                result += Stocks.Stocks(i).getOneTickerResponse()
            return result

        def SendEmail(from_, message):
            if from_ == '8482619494@mms.att.net':
                GroupMe.GroupMe('Quotes', message)
            elif from_ == '8482612817@mms.att.net':
                GroupMe.GroupMe('jacobson', message)
            else:
                email.sendserver.sendmail(
                    email.username, from_, message)
            print(f"{time.asctime()}\n{from_}\n{message}")

        def OneInputResponse(tick, user):
            ticker = tick[0]
            if len(ticker) >= 3 and ticker[:2] == "WL":
                listnum = Stocks.Stocks(ticker).watchLists()
                wl = db.DB(listnum, user).getWLByUser()
                response = WlProcesser(wl, user)
                SendEmail(user, response)
            else:
                db.DB(ticker, user).newUse()
                SendEmail(user, Stocks.Stocks(ticker).getOneTickerResponse())

        def TwoInputResponse(input, user):
            ticker = input[0]
            func = input[1]
            if (func == 'DHL'):
                response = Stocks.Stocks(ticker).dayHighLow()
                SendEmail(user, response)
        #########################
        testUser = 'paperstocksnj@gmail.com'

        testPass = "oeurjrdemmeyrffb"
        ##########################

        emailUserName = 'lakewoodnjQuotes@gmail.com'

        emailPassword = 'hlxnxrjvtgxeijky'

        email = Emails.LogIn(testUser, testPass)
        from_, tick = email.GetDataAndFroms()
        # print(from_,tick)
        db = MongoDB

        for i, user in enumerate(from_):
            try:
                tickLen = len(tick[i])
                if (tickLen == 1):
                    OneInputResponse(tick[i], user)
                elif (tickLen == 2):
                    print(tickLen)
                    TwoInputResponse(tick[i], user)
                elif (tickLen >= 3):
                    SendEmail(user, "sorry Working on some bugs")
            except Exception as e:
                # print(str(e))
                SendEmail('8482262840@mms.att.net', f"ERROR: {str(e)}")
    except e:
        print(e)
        

schedule.every(10).seconds.do(Main)

while 1:
    schedule.run_pending()
    time.sleep(1)
