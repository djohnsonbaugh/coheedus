from enum import Enum

class Notification(Enum):
    Incremented = 0
    Losing = 1
    Winning = 2
    Disabled = 3
    Overriden = 4
    Canceled = 5
    ProxyBid = 6

class BidState(Enum):
    Submitted = 0
    Losing = 1
    Winning = 2

class Bid(object):
    """description of class"""



    def __init__(self,id:int, aucid:int, sender:str, bidder:str, item:str, bid:int, max: int, increment: int):
        self.__ID:int = id
        self.__aucID:int = aucid
        self.__sender:str = sender
        self.__bidder:str = bidder
        self.__disabled:bool = False
        self.__override:bool = False
        self.__canceled:bool = False
        self.__item:str = item
        self.__bidMin:int = bid
        self.__bid:int = bid
        self.__bidLast:int = bid
        self.__bidMax:int = max if max > bid else bid
        self.__increment:int = increment if increment >= -1 else 0
        self.__notified:[bool] = [True, True, True, True, True, True, True]
        self.__bidstate:BidState = BidState.Submitted
        if bidder != sender:
            self.__QueNotification(Notification.ProxyBid)
        return


    def __NotificationNeeded(self, notif:Notification)->bool:
        return not self.__notified[notif.value]
    #PROPERTIES
    @property
    def ID(self)->int: return self.__ID
    @property
    def AucID(self)->int: return self.__aucID
    @property
    def Sender(self)->str: return self.__sender
    @property
    def Active(self)->bool: return not self.__canceled and not self.__disabled
    @property
    def Canceled(self)->bool: return self.__canceled
    @property
    def Bidder(self)->str: return self.__bidder
    @property
    def Item(self)->str: return self.__item
    @property
    def Bid(self)->int: return self.__bid
    @property
    def BidOriginal(self)->int: return self.__bidMin
    @property
    def BidLast(self)->int: return self.__bidLast
    @property
    def BidMax(self)->int: return self.__bidMax
    @property
    def Increment(self)->int: return self.__increment
    @property
    def IncrementStr(self)->str: return "Primes" if (self.Increment == -1) else self.Increment.__str__()
    @property
    def IsIncrementBid(self)->bool: return (self.__increment != 0)
    @property
    def IsPreBid(self)->bool: return (self.__aucID < 0)
    @property
    def Winning(self)->bool: return (self.__bidstate == BidState.Winning)
    @property
    def ToStr(self)->str: return self.__str__()
    @property
    def ProxyNotificationNeeded(self)->bool: return self.__NotificationNeeded(Notification.ProxyBid)
    @property
    def NotificationNeeded(self)->bool: 
        needed:bool = False
        for n in Notification:
            needed = needed or self.__NotificationNeeded(n)
        return needed
    @property
    def HasNotifications(self)->bool:
        for b in self.__notified:
            if(not b): return True
        return False
    @property
    def Disabled(self)->bool: return self.__disabled
    def Overriden(self)->bool: return self.__override

    def Disable(self): 
        self.__disabled = True
        self.QueNotification(Notification.Disabled)
        return
    def OverrideDisable(self): 
        self.__disabled = False
        self.__override = True
        self.QueNotification(Notification.Overrided)
        return

    def __getNextPrime(lowbid: int):
        if(lowbid % 2 == 0): lowbid -= 1
        prime:bool = False
        while not prime:
            lowbid += 2
            prime = True
            for i in range (3, lowbid -2, 2):
                if(lowbid % i == 0):
                    prime = False
                    break

        return lowbid

    def Cancel(self):
        self.__canceled = True
        self.QueNotification(Notification.Canceled)
        return

    def Equals(self, bid:Bid)->bool:
        return (
            self.Bidder == bid.Bidder and
            self.BidOriginal == bid.BidOriginal and
            self.BidMax == bid.BidMax and
            self.Increment == bid.Increment
        )

    def __QueNotification(self, notif:Notification):
        self.__notified[notif.value] = False
        return
    def __ClearNotification(self, notif:Notification):
        self.__notified[notif.value] = True
        return

    @Winning.setter
    def Winning(self,value:bool)->bool: 
        newstate:BidState = BidState.Winning if value == True else BidState.Losing
        #If state has changed, update state and setup a notification
        if(newstate != self.__bidstate):
            self.__ClearNotification(Notification.Winning)
            self.__ClearNotification(Notification.Losing)
            self.__bidstate = newstate
            self.__QueNotification(Notification(self.__bidstate.value))



    def GetProxyNotificaiton(self)->str:
        self.__ClearNotification(Notification.ProxyBid)
        return "Proxy Bid by " + bid.Sender + "->" + bid.ToStr

    def GetNotificationAndClear(self) ->str:
        notif:str = ""
        if(self.__NotificationNeeded(Notification.Disabled)): 
            notif += "Bid Disabled Due to Overbid, Repeat Bid To Override->"
            self.__ClearNotification(Notification.Disabled)
        elif(self.__NotificationNeeded(Notification.Canceled)): 
            notif += "Canceled->"
            self.__ClearNotification(Notification.Canceled)
        else:
            if(self.__NotificationNeeded(Notification.Losing)): 
                notif += "OUTBID!->"
                self.__ClearNotification(Notification.Losing)
            if(self.__NotificationNeeded(Notification.Winning)): 
                notif += "Winning->"
                self.__ClearNotification(Notification.Winning)
            if(self.__NotificationNeeded(Notification.Incremented)): 
                notif += "Auto Incremented->" + self.BidLast.__str__() + "->" + self.Bid.__str__()
                self.__ClearNotification(Notification.Incremented)
            if(self.__NotificationNeeded(Notification.Overriden)): 
                notif += "Overbid Overriden->"
                self.__ClearNotification(Notification.Overriden)
        notif += " " + self.ToStr
        return notif

    def IncrementBid(self, lowbid:int)->bool:
        if(lowbid >= self.BidMax): return False
        #Save last bid since last notification
        if not self.__NotificationNeeded(Notification.Incremented): self.__bidLast = self.Bid
        #Update Bid
        self.__bid = min(self.BidMax, self.__getNextPrime(lowbid) if self.Increment == -1 else lowbid + self.Increment)
        #Que Notification
        self.QueNotification(Notification.Incremented)
        return True

    #[PreBid bidID:-18] Girdle of the Fleet @ 10 for Dwendrox
    #[aucID:3 bidID:0]  Girdle of the Fleet  @ 5 for Dwendrox
    #[PreBid bidID:-2] Ring of Ire Intent @ 5 for Bigrax up to 20 by 3
    def __str__(self):
        bidstring: str = "["
        bidstring += "PreBid" if self.IsPreBid else "AucID:" + self.AucID.__str__()
        bidstring += " BidID:" + self.ID.__str__()
        bidstring += "] " + self.Item + " @ "
        bidstring += self.Bid.__str__()
        bidstring += " for " + self.Bidder
        if(self.IsIncrementBid):
            bidstring += " up to " + self.BidMax.__str__()
            bidstring += " by " + self.IncrementStr

        return bidstring

    #DEBUG representation of Bid
    def __repr__(self):
        bidstring: str = "["
        bidstring += self.AucID.__str__()
        bidstring += "," + self.ID.__str__()
        bidstring += "]" + self.Item + "@"
        bidstring += self.Bid.__str__()
        if(self.IsIncrementBid):
            bidstring += "->" + self.BidMax.__str__()
            bidstring += "," + self.IncrementStr
        bidstring += "[" + self.Sender
        if(self.Sender == self.Bidder):
            bidstring += "->" + self.Bidder
        bidstring += "]"

        return bidstring