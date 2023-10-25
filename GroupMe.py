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


def GroupMe(chatName, message):
    c = Client.from_token(
        'CbxaV0Qczv3ahCaK0nagt73fJI4pgrjpRA1O8puc')
    g = list(c.groups.list_all())
    for g in g:
        if g.name == chatName:
            g.post(message)
            break
