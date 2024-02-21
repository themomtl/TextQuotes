import finnhub


class Stocks:
    
    __finnhub_client = finnhub.Client(api_key="")
    def __init__(self,ticker):
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
    def getCompanyName(self):
        raw = self.__finnhub_client.company_profile2(symbol=f'{self.__ticker}')
        if 'name' in raw:
            return raw['name']
        else:
            return self.__ticker
    def getOneTickerResponse(self):
        result = f"{self.getCompanyName()}\n"
        result += f"Price: {self.getPrice()}\n"
        result += f"Change: ${self.getChange()}\n"
        result += f"Percent Change: {self.getPercentChange()}%\n"
        result += f"Previous Close: ${self.getPreviousClose()}\n"
        return result
    def dayHighLow(self):
        result = f"{self.__ticker}\n"
        result += f"Price: {self.getPrice()}\n"
        result += f"Day Low {self.__raw['l']}\n"
        result += f"Day High {self.__raw['h']}\n"
        return result
    def watchLists(self):
        wl = int(self.__ticker.strip('WL'))
        return wl

    