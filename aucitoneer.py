class Aucitoneer(object):
    """description of class"""

    def __init__(self,auctionchan:str):
        self.__aucchan = auctionchan

    @property
    def AuctionChannel(self)->str: return self.__aucchan
    @AuctionChannel.setter
    def AuctionChannel(self,value:str): self.__aucchan = value
