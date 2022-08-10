from auction import Auction
from bid import Bid
import eqApp
from datetime import datetime, timedelta
class Auctioneer(object):
    """description of class"""

    def __init__(self,auctionchan:str, maxactiveauctions:int):
        self.__aucchan = auctionchan
        self.__adminchan = ""
        self.__maxaucs = maxactiveauctions
        self.__auctions:{int,Auction} = {}
        self.__auccount = 0

        return
    def SendAuctionMessage(self, message:str):
        eqApp.sendMessage(self.__aucchan, message)
        return
    def SendAdminMessage(self, message:str):
        eqApp.sendMessage(self.__adminchan, message)
        return
    def NotifyBidder(self, bid:Bid, marginalbid:int):
        eqApp.tell(bid.Sender, bid.GetNotificationAndClear(marginalbid))
    def NotifyProxyBidder(self, bid:Bid):
        eqApp.tell(bid.Bidder, bid.GetProxyNotification())

    @property
    def IDAll(self)->int: return -300
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

    def __GetNextAucID(self)->int:
        self.__auccount += 1
        return self.__auccount - 1

    def FindUnClosedAuction(self, itemname:str)->Auction:
        auctionsearch:Auction = None
        for a in self.__auctions.values():
            if a.ItemName == itemname and not a.Closed:
                auctionsearch = a
                break
        return auctionsearch

    def AddAuction(self, items:[str], minutes: float=3.0, itemcount: int=1, autostart:bool=False, autoaward:bool=False)->str:
        updatedbids = ""
        #CHECK IF THIS AUCTION EXISTS ALREADY
        for i,item in enumerate(list(items)):
            auctionsearch:Auction = self.FindUnClosedAuction(item)
            if auctionsearch is not None:
                auctionsearch.Update(itemcount, minutes,autostart,autoaward)
                if(len(items) == 1):
                    return "Updated Auction->" + auctionsearch.ToStr
                if(updatedbids != ""): updatedbids += ","
                updatedbids += str(auctionsearch.ID)
            else:
                #ADD NEW AUCTION
                id = self.__GetNextAucID()
                self.__auctions[id] = Auction(id,item,itemcount,minutes,autostart,autoaward)
                if(len(items) == 1):
                    return "Created Auction->" + self.__auctions[id].ToStr
                if(updatedbids != ""): updatedbids += ","
                updatedbids += str(id)
        return "Auctions Created or Updated [" + updatedbids + "]"

    def AddBid(self, aucid:int, sender:str, bidder:str, item:str, bidderdkp:float, bid:int, max: int, increment: int)->str:
        if aucid == -1:
            #CHECK IF THIS AUCTION EXISTS ALREADY
            auctionsearch:Auction = self.FindUnClosedAuction(item)
            if auctionsearch is not None:
                aucid = auctionsearch.ID
            else:
                aucid = self.__auccount
                self.SendAdminMessage("VALIDATE->" + self.AddAuction([item]))
        if aucid in self.__auctions.keys():
            if self.__auctions[aucid].Closed: return "Auction[" + str(aucid) + "] is closed."
            else: return self.__auctions[aucid].AddBid(sender, bidder, self.__auctions[aucid].ItemName, bidderdkp, bid, max, increment)
        return "Auction[" + str(aucid) + "] does not exist."

    def __StartAuction(self, aucid:int, minutes: float=-1.0, itemcount: int=-1, autoaward:bool=False)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Update(itemcount, minutes,True,autoaward)
            return "Auction[" + str(aucid) + "] scheduled to begin."
        return "Auction[" + str(aucid) + "] does not exist."

    def StartAuction(self, aucid:int, minutes: float=-1.0, itemcount: int=-1, autoaward:bool=False)->str:
        if aucid == self.IDAll:
            ids:str = ""
            for auction in self.__auctions.values():
                if auction.ReadToSchedule:
                    ids += "" if ids == "" else ","
                    ids += str(auction.ID)
                    self.__StartAuction(auction.ID,minutes,itemcount,autoaward)
            return "Auctions[" + ids + "] scheduled to begin."
        else:
            return self.__StartAuction(aucid,minutes,itemcount,autoaward)

    def __CloseAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Close()
            return "Auction[" + str(aucid) + "] Closing..."
        return "Auction[" + str(aucid) + "] does not exist."

    def CloseAuction(self, aucid:int)->str:
        if aucid == self.IDAll:
            ids:str = ""
            for auction in self.__auctions.values():
                if auction.Closable:
                    ids += "" if ids == "" else ","
                    ids += str(auction.ID)
                    self.__CloseAuction(auction.ID)
            return "Auctions[" + ids + "] Closing..."
        else:
            return self.__CloseAuction(aucid)

    def __PauseAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Pause()
            return "Auction[" + str(aucid) + "] Pausing..."
        return "Auction[" + str(aucid) + "] does not exist."

    def PauseAuction(self, aucid:int)->str:
        if aucid == self.IDAll:
            ids:str = ""
            for auction in self.__auctions.values():
                if auction.Closable:
                    ids += "" if ids == "" else ","
                    ids += str(auction.ID)
                    self.__PauseAuction(auction.ID)
            return "Auctions[" + ids + "] Pausing..."
        else:
            return self.__PauseAuction(aucid)

    def __AwardAuction(self, aucid:int, autoaward:bool=True)->str:
        if aucid in self.__auctions.keys():
            self.__auctions[aucid].Award(autoaward)
            return "Auction[" + str(aucid) + "] have updated auto award status."
        return "Auction[" + str(aucid) + "] does not exist."

    def AwardAuction(self, aucid:int, autoaward:bool=True)->str:
        if aucid == self.IDAll:
            ids:str = ""
            for auction in self.__auctions.values():
                if not (auction.Awarded and auction.Closed):
                    ids += "" if ids == "" else ","
                    ids += str(auction.ID)
                    self.__AwardAuction(auction.ID,autoaward)
            return "Auctions[" + ids + "] have updated auto award status."
        else:
            return self.__AwardAuction(aucid, autoaward)

    def __CancelAuction(self, aucid:int)->str:
        if aucid in self.__auctions.keys():
            self.__auctions.pop(aucid)
            return "Auction[" + str(aucid) + "] has been canceled."
        return "Auction[" + str(aucid) + "] does not exist."

    def CancelAuction(self, aucid:int)->str:
        if aucid == self.IDAll:
            idsstr:str = ""
            ids:[int] = []
            for auction in self.__auctions.values():
                if not (auction.Awarded and auction.Closed):
                    ids.append(auction.ID)
            for id in ids:
                idsstr += "" if idsstr == "" else ","
                idsstr += str(id)
                self.__CancelAuction(id)
            return "Auctions[" + idsstr + "] have been canceled."
        else:
            return self.__CancelAuction(aucid)


    def ClearAuctionsAndBids(self)->str:
        self.__auctions = {}
        return "All Auctions & Bids Cleared."

    def __getActiveAuctionsCount(self):
        count = 0
        for a in self.__auctions.values():
            if a.Active: count += 1

        return count

    def __getAvailableAuctions(self)->[Auction]:
        auctions:[Auction] = []
        for auction in self.__auctions.values():
            if not (auction.Closed and auction.Awarded) and auction.Scheduled:
                auctions.append(auction)
        return auctions

    def Announce(self)->int:
        minute = timedelta(seconds=60)
        longwait = timedelta(seconds=45)
        medwait = timedelta(seconds=30)
        shortwait = timedelta(seconds=15)
        microwait = timedelta(seconds=5)
        zero = timedelta(0)
        messagecount = 0
        #NOTIFY PROXY BIDDERS
        for auction in self.__auctions.values():
            for bid in auction.GetProxyBidNotifications():
                self.NotifyProxyBidder(bid)
                messagecount += 1
        #NOTIFY BIDDERS
        for auction in self.__auctions.values():
            for bid in auction.GetBidNotifications():
                self.NotifyBidder(bid, auction.MarginalBid)
                messagecount += 1
        
        #UNAWARD RESTARTED AUCTIONS
        for auction in self.__auctions.values():
            if auction.Awarded and not auction.Closed:
                for message in auction.UnAward():
                    self.SendAuctionMessage(message)
                messagecount += 1
        
        auctioncount = self.__getActiveAuctionsCount()
        for auction in self.__getAvailableAuctions():
            if auctioncount < self.__maxaucs or auction.Active:
                newstart:bool = False
                if not auction.Active:
                    newstart = True
                    if auction.Restarted:
                        self.SendAuctionMessage("=====RESTARTING AUCTION <<" + auction.ItemName + ">>=====")
                    else:
                        self.SendAuctionMessage("=====NEW AUCTION STARTING <<" + auction.ItemName + ">>=====")
                    messagecount += 1
                    auctioncount += 1
                if (auction.TimeLeft > minute + medwait):
                    if (auction.TimeSinceLastAnnouncement > longwait) or (auction.TimeSinceLastAnnouncement > auction.TimeSinceLastBid and auction.TimeSinceLastBid > microwait) or newstart:
                        message = "Accepting Bids - "
                        self.SendAuctionMessage(message + auction.Announce())
                        messagecount += 1
                elif auction.TimeLeft >= medwait:
                    if(auction.TimeSinceLastAnnouncement > medwait) or (auction.TimeSinceLastAnnouncement > auction.TimeSinceLastBid and auction.TimeSinceLastBid > microwait):
                        message = "2nd Call Bids - "
                        self.SendAuctionMessage(message + auction.Announce())
                        messagecount += 1
                elif (auction.TimeLeft < medwait and auction.TimeLeft > zero)  or (auction.TimeSinceLastAnnouncement > auction.TimeSinceLastBid and auction.TimeSinceLastBid > microwait):
                    if auction.TimeSinceLastAnnouncement > shortwait:
                        message = "FINAL CALL Bids - "
                        self.SendAuctionMessage(message + auction.Announce())
                        messagecount += 1
                else:
                    if auction.TimeLeft <= zero:
                        if not auction.Closed:
                            self.SendAuctionMessage(auction.AnnounceClosed())
                            self.SendAdminMessage("Ready To Award:" + auction.WinnerSummary)
                            messagecount += 1
                        else:
                            if auction.ReadyToAward:
                                for message in auction.AnnounceAward():
                                    self.SendAuctionMessage(message)
                                    messagecount += 1

        return messagecount