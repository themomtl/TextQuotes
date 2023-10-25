import finnhub


class Stocks:
    
    __finnhub_client = finnhub.Client(api_key="c6s0ql2ad3ifcngb8qvg")
    def __init__(self,ticker):
        #self.__address = address
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
        result = f"{self.__ticker}\n"
        result += f"Price: {self.getPrice()}\n"
        result += f"Change: ${self.getChange()}\n"
        result += f"Percent Change: {self.getPercentChange()}%\n"
        result += f"Previous Close: ${self.getPreviousClose()}\n"
        return result
    def watchLists(self):
        wl = int(self.__ticker.strip('WL'))
        return wl

    