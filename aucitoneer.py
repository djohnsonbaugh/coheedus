class Aucitoneer(object):
    """description of class"""

    def __init__(self,adminchan:str, auctionchan:str):
        self.__adminchan = adminchan
        self.__aucchan = auctionchan

    @property
    def AdminChannel(self)->str: return self.__adminchan
    @AdminChannel.setter
    def AdminChannel(self,value:str): self.__adminchan = value

    @property
    def AuctionChannel(self)->str: return self.__aucchan
    @AdminChannel.setter
    def AuctionChannel(self,value:str): self.__aucchan = value
