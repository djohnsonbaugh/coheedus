from datetime import datetime, timedelta
import json
from typing import List
from unicodedata import decimal
from CharacterService import CharacterService
from Models.API_CharacterInfo import ApiCharInfo
from Models.API_Item import ApiItem
from Models.API_RaidTemplate import ApiRaidTemplate
from Models.API_RaidTick import ApiRaidTick
from appConfig import appConfig
from openDKP import openDKP
from Models.API_Raid import ApiRaid


class RaidService (object):
    """Current Raid Updating Utility"""
    
    
    def AlertMessages(self)->List[str] : return self.alertMessages
   
    def __init__(self):
        conf: appConfig = appConfig()
        self.__savepoint: ApiRaid = None
        self.__currentRaid:ApiRaid = None
        self.oDKP : openDKP = openDKP(conf)
        self.alertMessages: List[str] = []
        self.charService: CharacterService = CharacterService()
        self.exportFile:str = conf.get("OPENDKP","raidexportfile", "raid-export.txt")
    
    
    def checkCurrentRaid(self) -> bool:
        if(self.__currentRaid == None):
            raise Exception("No raid is loaded")


    def loadRaid(self, raidId:int)-> int:
        """Load raid from DKP Site"""
        #Clear out current raid incase it exists
        self.__currentRaid = None
        self.__savepoint = None

        loadedRaid: ApiRaid = self.oDKP.loadRaidById(raidId)
        # FIXME  TypeError: '<' not supported between instances of 'property' and 'datetime.datetime'
        # error if raid is > 1 day old
      #  if(loadedRaid.UpdatedTime < (datetime.utcnow() - timedelta(days = 1))):
      #     self.AlertMessages.append("Failed to load raid. Can't load raid updated over 1 day ago")
      #     print('Loaded raid is older than 1 day old')
      #     return -1

        self.__currentRaid = loadedRaid
        self.__savepoint = self.__currentRaid    
        return self.__currentRaid.IdRaid

    def createRaid(self, raidName:str) -> int:
        """Start a new raid from the default template set in the configs"""
        #Clear out current raid incase it exists
        self.__currentRaid = None
        self.__savepoint = None

        template: ApiRaidTemplate = self.oDKP.loadDefaultRaidTemplate()
        newRaid = ApiRaid()
        newRaid.Name = raidName
        for tick in template.Ticks:
            newRaid.Ticks.append(tick)
        newRaid.Attendance = 1 #FIXME Will Attendance always  be True?
        newRaid.Items = []

        self.__currentRaid: ApiRaid= self.oDKP.pushRaid(newRaid)
        return self.__currentRaid.IdRaid


  
    def addItems(self, charName:str, dkpAmt:decimal, itemName:str, notes:str, pushRaid:bool):
        self.checkCurrentRaid()           
        item = ApiItem()
        item.CharacterName = charName
        item.IdCharacter = self.charService.getCharacterId(charName)
        item.DkpValue = dkpAmt   #DKP Spent
        item.ItemName = itemName
        item.Notes = '' if notes == None else notes # Auction ID?

        itemResponse = self.oDKP.lookupItem(itemName=itemName)
        item.GameItemId = itemResponse["GameItemId"]
        item.ItemID = itemResponse["ItemID"]

        self.__currentRaid.Items.append(item)

        if(pushRaid == None or pushRaid):
            self.pushRaid()

        return

    
    def createRaidTick(self, tickDescription, dkpValue, attendees:List[str], boxTick:bool,  pushRaid:bool):
        self.checkCurrentRaid()
        newTick = ApiRaidTick()
        for tick in self.__currentRaid.Ticks:
            if (tick.Description == tickDescription):
                newTick = tick
                self.__currentRaid.Ticks.remove(tick)
       
        
        newTick.RaidId = self.__currentRaid.IdRaid
        newTick.Description = tickDescription
        newTick.Value = dkpValue

        for s in attendees:
            if (boxTick or self.charService.isMain(s)):
                newTick.Attendees.append(s)
        
        self.__currentRaid.Ticks.append(newTick)

        if(pushRaid == None or pushRaid):
            self.pushRaid()
        return

    def pushRaid(self):
        """Push Raid to website"""
        self.checkCurrentRaid()
        self.oDKP.pushRaid(self.__currentRaid)
        self.__savepoint = self.__currentRaid
        return
    
    def getLastSavePoint(self) -> ApiRaid:
        return self.__savepoint

    def getCurrentRaid(self) -> ApiRaid:
        return self.__currentRaid

    def saveRaidToFile(self):
        if(self.__currentRaid == None):
            #self.AlertMessages.append('Failed to export raid to file. No Raid loaded.')
            print('Error exporting to file')
            return

        f = open(self.exportFile, "a")
        f.write(self.__currentRaid.toJson())
        f.close()
        return

    def loadRaidFromFile(self) -> int:   
        #Clear out current raid incase it exists
        self.__currentRaid: ApiRaid = None
        self.__savepoint: ApiRaid  = None

        f = open(self.exportFile, "a")
        self.__currentRaid: ApiRaid  = ApiRaid.from_json(f.read)
        f.close()
        return self.__currentRaid.IdRaid