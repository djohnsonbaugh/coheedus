from bid import Bid
class Auction(object):
    """description of class"""
    def __init__(self,id:int, item:str, itemcount:int, minutes:float, autostart:bool=False, autoaward:bool=False):
        self.__ID:int = id
        self.__item:str = item
        self.__itemcount:int = itemcount
        self.__minutes:float = minutes
        self.__bids:[Bid] = []
        self.__winners:[Bid] = []
        self.__autostart:bool = autostart
        self.__autoaward:bool = autoaward
        self.__closed:bool = False
        return
    
    #PROPERTIES
    @property
    def ID(self)->int: return self.__ID
    @property
    def BidCount(self)->int: return len(self.__bids)
    @property
    def MarginalBid(self)->int:
        if(len(self.__winners) == 0): return 0
        return self.__winners[len(self.__winners)-1].Bid
    @property
    def ItemCount(self)->int: return self.__itemcount
    @property
    def Closed(self)->bool: return self.__closed

    def __IsWinning(bid:Bid):
        for b in self.__winners:
            if b.ID == bid.ID:
                return True
        return False

    def __CalculateWinners(self):
        winners: [Bid] = []
        for bid in self.__bids:
            if bid.Disabled: continue
            insertindex = 0
            #Find Rank of Bid for winners so far
            for winbid in winners:
                if(bid.Bid > winbid.Bid):
                    break
                insertindex += 1
            #Add Bid to the end if not enough winners
            if insertindex >= len(winners): 
                if insertindex < self.ItemCount:
                    winners.append(bid)
            #Insert bid into winners and remove previous winner
            else:
                winners.insert(insertindex, bid)
                if len(winners) > self.ItemCount:
                    winners.pop()

        self.__winners = winners
        return

    def __IncrementBids(self)->bool:
        recaculate:bool = False
        for bid in self.__bids:
            if(bid.IsIncrementBid and bid.BidMax > self.MarginalBid):
                 if(not self.__IsWinning(bid)):
                     bid.IncrementBid(self.MarginalBid)
        return recaculate

    def __Calculate(self):
        while True:
            self.__CalculateWinners()
            if(not self.__IncrementBids()): break
        for bid in self.__bids:
            bid.Winning = self.__IsWinning(bid)

    def AddBid(self, newbid:Bid)->str:
        self.__bids.append(newbid)
        self.__Calculate()
        return newbid.GetNotificationAndClear()

    def AddBid(self, sender:str, bidder:str, item:str, bid:int, max: int, increment: int)->str:
        newbid:Bid = Bid(self.BidCount, self.__ID, sender, bidder, item, bid, max, increment)
        return self.AddBid(newbid)







