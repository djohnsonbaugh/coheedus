class Aucitoneer(object):
    """description of class"""

    def __init__(self,auctionchan:str, maxactiveauctions:int):
        self.__aucchan = auctionchan
        self.__maxaucs = maxactiveauctions
        self.__auctions:[Auction] = []

        return


    @property
    def AuctionChannel(self)->str: return self.__aucchan
    @AuctionChannel.setter
    def AuctionChannel(self,value:str): self.__aucchan = value

    @property
    def MaxActiveAuctions(self)->int: return self.__maxaucs
    @MaxActiveAuctions.setter
    def MaxActiveAuctions(self,value:int): self.__maxaucs = value

    def AddAuction(self, item:str, minutes: float=3.0, itemcount: int=1, autostart:bool=False, autoaward:bool=False)->str:

        return "Not Implemented"

    def AddBid(self, aucid:int, sender:str, bidder:str, item:str, bid:int, max: int, increment: int)->str:

        return "Not Implemented"

    def StartAuction(self, aucid:int, minutes: float=-1.0)->str:

        return "Not Implemented"

    def CloseAuction(self, aucid:int)->str:

        return "Not Implemented"

    def PauseAuction(self, aucid:int)->str:

        return "Not Implemented"

    def ClearAuctionsAndBids(self)->str:

        return "Not Implemented"