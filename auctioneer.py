from auction import Auction
from bid import Bid
import eqApp
class Auctioneer(object):
    """description of class"""

    def __init__(self,auctionchan:str, maxactiveauctions:int):
        self.__aucchan = auctionchan
        self.__adminchan = ""
        self.__maxaucs = maxactiveauctions
        self.__auctions:{int,Auction} = {}

        return


    @property
    def AuctionChannel(self)->str: return self.__aucchan
    @AuctionChannel.setter
    def AuctionChannel(self,value:str): self.__aucchan = value
    @property
    def AdminChannel(self)->str: return self.__adminchan
    @AdminChannel.setter
    def AdminChannel(self,value:str): self.__adminchan = value

    @property
    def MaxActiveAuctions(self)->int: return self.__maxaucs
    @MaxActiveAuctions.setter
    def MaxActiveAuctions(self,value:int): self.__maxaucs = value

    def FindUnClosedAuction(self, itemname:str, auctionsearch:Auction)->bool:
        for a in reversed(self.__auctions.values):
            if a.ItemName == itemname and not a.Closed:
                auctionsearch = a
                return True
        return False

    def AddAuction(self, item:str, minutes: float=3.0, itemcount: int=1, autostart:bool=False, autoaward:bool=False)->str:
        #CHECK IF THIS AUCTION EXISTS ALREADY
        auctionsearch:Auction
        if FindUnClosedAuction(item, auctionsearch):
            auctionsearch.Update(itemcount, minutes,autostart,autoaward)
            return "Updated Auction->" + auctionsearch.ToStr
        #ADD NEW AUCTION
        id = len(self.__auctions)
        self.__auctions[id] = Auction(id,item,itemcount,minutes,autostart,autoaward)
        return "Created Auction->" + self.__auctions[id].ToStr

    def AddBid(self, aucid:int, sender:str, bidder:str, item:str, bidderdkp:float, bid:int, max: int, increment: int)->str:
        if aucid == -1:
            return "Prebid not implemented."
        if aucid in self.__auctions.keys():
            if self.__auctions[aucid].Closed: return "Auction[" + aucid + "] is closed."
            else: return self.__auctions[aucid].AddBid(sender, bidder, item, bid, max, increment)
        return "Auction[" + aucid + "] does not exist."

    def StartAuction(self, aucid:int, minutes: float=-1.0, itemcount: int=-1, autoaward:bool=False)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Update(itemcount, minutes,True,autoaward)
            return "Auction[" + aucid + "] scheduled to begin."
        return "Auction[" + aucid + "] does not exist."

    def CloseAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Close()
            return "Auction[" + aucid + "] Closing..."
        return "Auction[" + aucid + "] does not exist."

    def PauseAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Pause()
            return "Auction[" + aucid + "] Pausing..."
        return "Auction[" + aucid + "] does not exist."

    def AwardAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Award()
            return "Auction[" + aucid + "] Awarding..."
        return "Auction[" + aucid + "] does not exist."

    def ClearAuctionsAndBids(self)->str:
        self.__auctions = {}
        return "All Auctions & Bids Cleared."

    def __getActiveAuctionsCount(self):
        count = 0
        for a in self.__auctions.values:
            if a.Active: count += 1

        return count

    def __getAvailableAuctions(self)->[Auction]:
        auctions[Auction] = []
        for auction in self.__auctions.values:
            if not auction.Closed and auction.Scheduled:
                auctions.append(auction)
        return auctions

    def SendAuctionMessage(self, message:str):
        eqApp.sendMessage(self.__aucchan, message)
        return
    def SendAdminMessage(self, message:str):
        eqApp.sendMessage(self.__adminchan, message)
        return
    def NotifyBidder(self, bid:Bid):
        eqApp.tell(bid.Sender, bid.GetNotificationAndClear())
    def NotifyProxyBidder(self, bid:Bid):
        eqApp.tell(bid.Bider, bid.GetProxyNotification())

    def Announce(self):
        minute = timedelta(seconds=60)
        longwait = timedelta(seconds=45)
        shortwait = timedelta(seconds=15)
        microwait = timedelta(seconds=5)
        zero = timedelta(0)

        #NOTIFY PROXY BIDDERS
        for auction in self.__auctions.values:
            for bid in auction.GetProxyBidNotifications():
                self.NotifyProxyBidder(bid)
        #NOTIFY BIDDERS
        for auction in self.__auctions.values:
            for bid in auction.GetBidNotifications():
                self.NotifyBidder(bid)
        
        #UNAWARD RESTARTED AUCTIONS
        for auction in self.__auctions.values:
            if auction.Awarded and not auction.Closed:
                for message in auction.UnAward():
                    SendAuctionMessage(message)
        
        auctioncount = self.__getActiveAuctionsCount()
        for auction in self.__getAvailableAuctions():
            if auctioncount < self.__maxaucs or auction.Active:
                if not auction.Active:
                    self.SendAuctionMessage("=====NEW AUCTION STARTING <<" + auction.ItemName + ">>=====")
                    auctioncount += 1
                if (
                    #NEW BID DELAY
                    (auction.TimeSinceLastAnnouncement > auction.TimeSinceLastBid and auction.TimeSinceLastBid > microwait) or
                    #EARLY AUCTION
                    (auction.TimeSinceLastAnnouncement > longwait and auction.TimeLeft >= minute and auction.TimeLeft > zero) or
                    #LATE AUCTION
                    (auction.TimeSinceLastAnnouncement > shortwait and auction.TimeLeft < minute and auction.TimeLeft > zero) or
                    #LAST CALL AUCTION
                    (auction.TimeLeft =< zero and auction.TimeSinceLastBid < shortwait)
                    ):
                    message = "Bids:" if auction.TimeLeft > 0 else "LAST CALL:"
                    SendAuctionMessage(message + auction.Announce())
                else:
                    if auction.TimeLeft =< zero:
                        if not auction.Closed:
                            SendAuctionMessage(auction.AnounceClosed())
                            SendAdminMessage("Ready To Award:" + auction.WinnerSummary)
                        else:
                            if auction.ReadyToAward:
                                for message in auction.Award():
                                    SendAuctionMessage(message)

        return