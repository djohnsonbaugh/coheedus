from Models.API_Item import ApiItem
from Models.API_RaidTick import ApiRaidTick
from .openDKP import openDKP
from .Models.API_Raid import ApiRaid


class RaidService (object):
    """Current Raid Updating Utility"""
    
    def __init__(self, oDKP):
        self.__savepoint: ApiRaid = None
        self.__currentRaid:ApiRaid = None
        self.oDKP : oDKP

    
    def checkCurrentRaid(self) -> bool:
        if(self.__currentRaid == None):
            raise Exception("No raid is loaded")


    def loadRaid(self, raidId):
        """Load raid from DKP Site"""


        #TODO error if raid is > 1 day old

        #TODO when template loaded, need to check for default attendence ticks. and auto genete raid dump at those time intervals
        return

    def createRaid(self) -> int:
        """Start a new raid from the default template set in the configs"""
        #TODO load raid template and save it to the DKP Site. 

        #TODO Store load raid object into class instance
        
        #TODO when template loaded, need to check for default attendence ticks. and auto genete raid dump at those time intervals
        return

  
    def addItems(self, charName, dkpAmt, itemName, notes, pushRaid):
        self.checkCurrentRaid()

        #TODO Figure out req params.
        item = ApiItem()
        item.CharacterName = ""
        item.DkpValue = 0.0   #DKP Spent
        item.ItemName = ""
        item.Notes = '' if notes == None else notes # Auction ID?

        
        ##TODO look up item too get Id
        item.GameItemId = -1
        item.ItemID = -1

        self.__currentRaid.Items.append(item)

        if(pushRaid == None or pushRaid):
            self.pushRaid()

        return

    #TODO figure out required parameters
    def createRaidTick(self, tickDescription, dkpValue, attendees:str[],  pushRaid:bool):
        self.checkCurrentRaid()
        
        tick = ApiRaidTick()
        tick.RaidId = self.__currentRaid.IdRaid
        tick.Description = tickDescription
        tick.Value = dkpValue
        tick.Attendees = attendees.copy()
        if(pushRaid == None or pushRaid):
            self.pushRaid()
        return

    def pushRaid(self):
        """Push Raid to website"""
        self.checkCurrentRaid()

        self.__savepoint = self.__currentRaid
        return