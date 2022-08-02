from bid import Bid
from datetime import datetime, timedelta
class Auction(object):
    """description of class"""
    def __init__(self,id:int, item:str, itemcount:int, minutes:float, autostart:bool=False, autoaward:bool=False):
        self.__ID:int = id
        self.__item:str = item
        self.__itemcount:int = itemcount
        self.__minutes:float = minutes
        self.__bids:[Bid] = []
        self.__winners:[Bid] = []
        self.__scheduled:bool = autostart
        self.__started:bool = False
        self.__autoaward:bool = autoaward
        self.__closed:bool = False
        self.__awarded:bool = False
        self.__lastAnnouncement:datetime = None
        self.__timeleft:timedelta = timedelta(minutes=minutes)
        self.__lastNewBid:datetime = datetime.min()
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
    def ItemName(self)->str: return self.__item
    @property
    def Closed(self)->bool: return self.__closed
    @property
    def Awarded(self)->bool: return self.__awarded
    @property
    def ReadyToAward(self)->bool: return self.__autoaward and not self.__awarded
    @property
    def Active(self)->bool: return self.__started and not (self.__closed and self.__awarded)
    @property
    def Scheduled(self)->bool: return self.__scheduled
    @property
    def LastNewBidTime(self)->datetime: return self.__lastNewBid
    @property
    def TimeSinceLastBid(self)->timedelta: return datetime.now() - self.__lastNewBid
    @property
    def TimeSinceLastAnnouncement(self)->timedelta: return datetime.now() - self.__lastAnnouncement
    @property
    def TimeLeft(self)->timedelta: return self.__timeleft
    @property
    def ToStr(self)->str: return self.__str__()

    def __IsWinning(bid:Bid):
        for b in self.__winners:
            if b.ID == bid.ID:
                return True
        return False

    def __CalculateWinners(self):
        winners: [Bid] = []
        for bid in self.__bids:
            if not bid.Active: continue
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

    def AddBidComplete(self, bid:Bid)->str:
        if self.__scheduled:
            self.__Calculate()
        return bid.GetNotificationAndClear()

    def FindAcitveBidToCancel(self, bidder:str, bidsearch:Bid) ->bool:
        for b in reversed(self.__bids):
            if b.Bidder == bidder and b.Active:
                bidsearch = b
                return True
        return False

    def GetProxyBidNotifications(self)->[Bid]:
        bids:[Bid] = []
        for b in self.__bids:
            if b.ProxyNotificationNeeded:
                bids.append(b)
        return bids

    def GetBidNotifications(self)->[Bid]:
        bids:[Bid] = []
        for b in self.__bids:
            if b.NotificationNeeded:
                bids.append(b)
        return bids

    def FindEqualBid(self, bid:Bid, bidsearch:Bid)->bool:
        for b in reversed(self.__bids):
            if bid.Equals(b):
                bidsearch = b
                return True 
        return False

    def AddBid(self, sender:str, bidder:str, item:str, bidderdkp:float, bid:int, max: int, increment: int)->str:
        bidsearch:Bid = None       
        
        #CANCEL BID
        if bid == 0:
            if FindAcitveBidToCancel(bidder, bidsearch):
                bidsearch.Cancel()
                return self.AddBidComplete(bidsearch)
            else:
                return "No active bids by " + newbid.Bidder + " for item " + self.__item + " were found to cancel."

        newbid:Bid = Bid(self.BidCount, self.__ID, sender, bidder, item, bid, max, increment)

        #CHECK IF THIS IS AN OVERRIDE
        if FindEqualBid(newbid, bidsearch):
            if bidsearch.Disabled and not bidsearch.Overriden:
                bidsearch.OverrideDisable()
                return self.AddBidComplete(bidsearch)

        #DISABLE OVERBIDDING
        if newbid.BidMax > bidderdkp:
            newbid.Disable()

        #ADD NEW BID
        self.__bids.append(newbid)      
        self.__lastNewBid = datetime.now()
        self.__timeleft += timedelta(seconds=10)
        return self.AddBidComplete(newbid)

    def Announce(self)->str:
        if self.__started:
            self.__timeleft -= datetime.now() - self.__lastAnnouncement
        else: self.__started = True
        self.__lastAnnouncement = datetime.now()
        return self.AnnounceStr

    def Pause(self):
        self.__started = False
        self.__scheduled = False
        self.__lastAnnouncement = datetime.min()
        return
    
    def Close(self):
        self.__timeleft = timedelta(0)
        self.__lastAnnouncement = datetime.min()
        self.__lastNewBid = datetime.min()

    def Award(self):
        self.__autoaward = True
        return

    def AnnounceClosed(self)->str:
        self.__closed = True
        return "Closed: " + self.AuctionStr

    def AnnounceAward(self)->[str]:
        wins:[str] = []
        for bid in self.__winners:
            wins.append("Winner - " + self.__item + " - " + self.MarginalBid + " - " + bid.Bidder)
        self.__awarded = True
        return

    def UnAward(self)->[str]:
        wins:[str] = []
        for bid in self.__winners:
            wins.append("Winner - " + self.__item + " - " + 0 + " - " + bid.Bidder)
        self.__awarded = False
        return 

    def Update(self, itemcount:int=-1, minutes:float=-1, autostart:bool=False, autoaward:bool=False):
        if(minutes > 0):
            self.__timeleft = timedelta(minutes=minutes)
        if(itemcount >0):
            self.__itemcount = itemcount
        self.__scheduled = True
        self.__started = False
        self.__autoaward = autoaward
        return

    @property
    def AuctionStr(self):
        aucstring: str = "[AucID:" + str(self.ID)
        aucstring += "] " + str(self.ItemCount)
        aucstring += "x <<" + self.Item
        aucstring += ">> "
        seconds = self.__timeleft.seconds
        mintues = seconds // 60
        seconds -= minutes * 60
        aucstring += '{:02}:{:02}'.format(int(minutes), int(seconds))
        aucstring += " Bids: "
        idstring += " [IDs:"
        if len(self.__winners) == 0: aucstring += "0"
        for i, bid in enumerate(list(self.__winners)):
            if i > 0: 
                aucstring += ","
                idstring += ","
            aucstring += str(bid.Bid)
            idstring += str(bid.ID)
        aucstring += idstring + "]"
        return aucstring

    @property
    def WinnerSummary(self):
        aucstring: str = "[AucID:" + str(self.ID)
        aucstring += "] " + str(self.ItemCount)
        aucstring += "x <<" + self.Item
        aucstring += ">> "
        aucstring += " Winning: "
        idstring += " ["
        if len(self.__winners) == 0: aucstring += "0"
        for i, bid in enumerate(list(self.__winners)):
            if i > 0: 
                aucstring += ","
                idstring += ","
            aucstring += str(bid.Bid)
            idstring += bid.Bidder
        aucstring += idstring + "]"
        return aucstring


    def __str__(self):
        aucstring: str = "[AucID:" + self.ID.__str__()
        aucstring += "] " + self.Item
        aucstring += " x" + self.ItemCount.__str__()
        return aucstring

    #DEBUG representation of Bid
    def __repr__(self):
        aucstring: str = "[" + self.ID.__str__()
        aucstring += "] " + self.Item
        aucstring += " x" + self.ItemCount.__str__()
        return aucstring






