from cgitb import html
from email import message
from hashlib import new
import smtplib
import email
import imaplib
from bs4 import BeautifulSoup
import nltk
import time


class LogIn():
    def __init__(self, username, password):
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
        result, data = self.mail.uid('search', None, 'UnSeen')
        new_items = data[0].split()
        return new_items

    def GetLength(self):
        return len(self.GetMail())

    def Token(self, Input):
        # makes any string to array
        Input = nltk.word_tokenize(Input)
        # converts that array to upper case
        # returns the upper case Array
        return [x.upper() for x in Input]

    def GetDataAndFroms(self):
        froms = []
        data = []
        if int(self.GetLength()) > 0:
            for x in self.GetMail():
                result2, email_data = self.mail.uid('fetch', x, '(RFC822)')
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                froms.append(email_message['From'])
                # text =''
                for part in email_message.walk():
                    # get content type of each part of the email
                    content_type = part.get_content_type()
                    # if the part is 'text/html' or 'text/html' exctract the email content
                    # if(content_type == 'text/html'):
                    msg_ = part.get_payload()
                    if content_type == 'text/html':
                        soup = BeautifulSoup(msg_, 'html.parser')
                        try:
                            # ATT
                            text = soup.td.get_text(strip=True).upper()
                        except:
                            # Emails
                            text = soup.div.get_text(strip=True).upper()
                    elif content_type == 'text/plain':
                        # VZ
                        text = msg_.strip().upper()
                    """else:
                        print('not a content type')"""
                # Append the parsed message to the list
                data.append(self.Token(text))
            return froms, data
        else:
            print(f"\nstocks\n{time.asctime()}\nNo mail")
            return froms, data

