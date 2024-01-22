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
from groupy import Client
import groupy



mainkey = 'CbxaV0Qczv3ahCaK0nagt73fJI4pgrjpRA1O8puc'
googleVoice = 'P4q9frX8NOvojQcCyb0kjuLRAzOxX9H32NJHR73C'
"""class Groupme():
    
    def __init__(self):
        self.GM = Client.from_token(
        googleVoice)
    
    def checkList(self,chatName):
        result = False
        listOfGroups = list(self.GM.groups.list_all())
        for group in listOfGroups:
            if group.name == chatName:
                return True , group
        return result, None
    def makeGroup(self,chatName):
        newGroup = self.GM.groups.create(name=f'{chatName}')"""
        
        
def GroupMe(chatName, message):
    c = Client.from_token(
        'CbxaV0Qczv3ahCaK0nagt73fJI4pgrjpRA1O8puc')
    listOfGroups = list(c.groups.list_all())
    for group in listOfGroups:
        if group.name == chatName:
            group.post(message)
        """else:
            print("Group not found")"""
