from cgitb import html
from email import message
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

emailUserName = 'paperstocksnj@gmail.com'

emailPassword = 'oeurjrdemmeyrffb'


class Emails():  
    def __init__(self , username , password):
        serverStart = 'imap.gmail.com'
        self.sendserver = smtplib.SMTP('smtp.gmail.com', 587)
        self.sendserver.starttls()
        self.mail = imaplib.IMAP4_SSL(serverStart)
        self.username = username
        self.password = password
        self.mail.login(self.username, self.password)
        self.sendserver.login(self.username, self.password)
    def GetMail(self):
        self.mail.select('Inbox')
        result, data = self.mail.uid('search',None, 'UnSeen')
        new_items = data[0].split()
        return new_items
    def GetLength(self):
        return len(self.GetMail())
    def Token(self, Input):
        #makes any string to array
        Input = nltk.word_tokenize(Input)
        #converts that array to upper case
        #returns the upper case Array
        return [x.upper() for x in Input]
    def GetDataAndFroms(self):
        froms =[]
        data = []
        if int(self.GetLength()) > 0:
            for x in self.GetMail():
                result2, email_data = self.mail.uid('fetch', x , '(RFC822)')
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                froms.append(email_message['From'])
                #text =''
                for part in email_message.walk():
                    # get content type of each part of the email
                    content_type = part.get_content_type()
                    #if the part is 'text/html' or 'text/html' exctract the email content
                    #if(content_type == 'text/html'): 
                    msg_ = part.get_payload()
                    if content_type =='text/html':
                        soup = BeautifulSoup(msg_,'html.parser')
                        try:
                            #ATT
                            text = soup.td.get_text(strip=True).upper() 
                        except:
                            #Emails
                            text = soup.div.get_text(strip=True).upper()
                    elif content_type == 'text/plain':
                        #VZ
                        text = msg_.strip().upper() 
                    """else:
                        print('not a content type')"""
                #Append the parsed message to the list    
                data.append(self.Token(text))  
            return froms, data
        else:
            print(f"\nstocks\n{time.asctime()}\nNo mail")  
            return froms, data
#print(Emails(emailUserName,emailPassword).GetDataAndFroms())


class Stocks:
    
    __finnhub_client = finnhub.Client(api_key="c6s0ql2ad3ifcngb8qvg")
    def __init__(self,ticker, address):
        self.__address = address
        self.__ticker = ticker
        self.__raw = self.__finnhub_client.quote(self.__ticker)
        
    def getPrice(self):
        return self.__raw['c'] 
    
    def getChange(self):
        return self.__raw['d']
    
    def getPercentChange(self):
        return self.__raw['dp']
    
    def getPreviousClose(self):
        return self.__raw['pc']   
    
    def getOneTickerResponse(self):
        result = f"{self.ticker}\n"
        result += f"Price: {self.getPrice()}\n"
        result += f"Change: ${self.getChange()}\n"
        result += f"Percent Change: {self.getPercentChange()}%\n"
        result += f"Previous Close: ${self.getPreviousClose()}\n"
        return result
    def watchLists(self):
        wl = int(self.__ticker.strip('WL'))
        return wl,self.__address


class DB:
    
    def __init__(self,ticker,address):
        self.__address = address
        self.__ticker = ticker
        self.__ca = certifi.where()
        self.__client = pymongo.MongoClient(
        "mongodb+srv://MYCoding:QV9BcLxtJqrInZB4@mycoding.pzucnk1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=self.__ca)
    def newUse(self):
        db = self.__client["Stocks"]
        collection = db["Users"]
        post = {"User": self.__address, "Ticker": self.__ticker}
        collection.insert_one(post)
        return 1
    def newWL(self):
        db = self.__client["Stocks"]
        collection = db["WL"]
        post = {"User": self.__address, "Tickers": self.__ticker}
        collection.insert_one(post)
        return 1
    def getWLByUser(self):
        db = self.__client["Stocks"]
        collection = db["WL"]
        document = collection.find({'User': self.__address}).skip(
            self.__ticker).limit(1)[0]["Tickers"].split(',')
        return document
    
    def getWlCount(self):
        db = self.__client["Stocks"]
        collection = db["WL"]
        query = {'User': self.__address}
        number = collection.count_documents(query)
        return str(number)

class Main:
    def __init__(self, email):
        