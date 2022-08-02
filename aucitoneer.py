class Aucitoneer(object):
    """description of class"""

    def __init__(self,auctionchan:str, maxauctions:int):
        self.__aucchan = auctionchan
        self.__maxaucs = maxactiveauctions
    @property
    def AuctionChannel(self)->str: return self.__aucchan
    @AuctionChannel.setter
    def AuctionChannel(self,value:str): self.__aucchan = value

    @property
    def MaxActiveAuctions(self)->int: return self.__maxaucs
    @MaxActiveAuctions.setter
    def MaxActiveAuctions(self,value:int): self.__maxaucs = value



