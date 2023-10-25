import pymongo
import certifi


class DB:

    def __init__(self, ticker, address):

        self.__address = address
        self.__ticker = ticker
        self.__ca = certifi.where()
        self.__client = pymongo.MongoClient(
            "mongodb+srv://MYCoding:QV9BcLxtJqrInZB4@mycoding.pzucnk1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=self.__ca)
        self.__db = self.__client["Stocks"]
        self.__userCollection = self.__db["Users"]
        self.__wlCollection = self.__db["WL"]

    def newUse(self):
        post = {"User": self.__address, "Ticker": self.__ticker}
        self.__userCollection.insert_one(post)
        return 1

    def newWL(self):
        post = {"User": self.__address, "Tickers": self.__ticker}
        self.__wlCollection.insert_one(post)
        return 1

    def getWLByUser(self):
        document = self.__wlCollection.find({'User': self.__address}).skip(
            self.__ticker).limit(1)[0]["Tickers"].split(',')
        return document

    def getWlCount(self):
        query = {'User': self.__address}
        number = self.__wlCollection.count_documents(query)
        return str(number)
