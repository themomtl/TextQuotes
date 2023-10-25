from cgitb import html
#from email import message
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

def Main():
    
    emailUserName = 'paperstocksnj@gmail.com'

    emailPassword = 'oeurjrdemmeyrffb'

    email = Emails.LogIn(emailUserName,emailPassword)            
    from_ ,tick = email.GetDataAndFroms()
    print(from_,tick)
    db = MongoDB

    def WlProcesser(wl):
        result = ""
        for i in wl:
            result += Stocks.Stocks(i).getOneTickerResponse()
        return result    
        

    for i, user in enumerate(from_):
        tickLen = len(tick[i])
        if( tickLen == 1):
            ticker = tick[i][0]
            if len(ticker) >= 3 and ticker[:2] == "WL":
                listnum = Stocks.Stocks(ticker).watchLists()
                wl = db.DB(listnum,user).getWLByUser()
                response = WlProcesser(wl)
                email.sendserver.sendmail(email.username,user,response)
            else:    
                db.DB(ticker,user).newUse()
                email.sendserver.sendmail(email.username,user,Stocks.Stocks(ticker).getOneTickerResponse())
        elif(tickLen >= 2):
            email.sendserver.sendmail(email.username,user,"sorry Working on some bugs")