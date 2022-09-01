import json
from typing import List
from unicodedata import decimal
from CharacterService import CharacterService
from Models.API_CharacterInfo import ApiCharInfo, CharRank
from Models.API_Item import ApiItem
from Models.API_RaidTick import ApiRaidTick
from .openDKP import openDKP
from .Models.API_Raid import ApiRaid


class RaidService (object):
    """Current Raid Updating Utility"""
   
    @property
    def CharacterService(self)->CharacterService: return self.characterService

    def __init__(self, oDKP):
        self.__savepoint: ApiRaid = None
        self.__currentRaid:ApiRaid = None
        self.oDKP : openDKP = oDKP
        self.__alertMessages: List[str] = List[str]
        self.charDict :dict[str,ApiCharInfo] = []
        self.characterService: CharacterService = CharacterService(oDKP=oDKP)

    
    
    def checkCurrentRaid(self) -> bool:
        if(self.__currentRaid == None):
            raise Exception("No raid is loaded")


    def loadRaidFromSite(self, raidId):
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

  
    def addItems(self, charName:str, dkpAmt:decimal, itemName:str, notes:str, pushRaid:bool):
        self.checkCurrentRaid()           
        item = ApiItem()
        item.CharacterName = charName
        item.IdCharacter = self.characterService.getCharacterId(charName) 
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

    
    def createRaidTick(self, tickDescription, dkpValue, attendees:[str],  pushRaid:bool):
        self.checkCurrentRaid()
        newTick = ApiRaidTick()
        for tick in self.__currentRaid.Ticks:
            if (tick.Description == tickDescription):
                newTick = tick
                self.__currentRaid.Ticks.remove(tick)
       
        
        newTick.RaidId = self.__currentRaid.IdRaid
        newTick.Description = tickDescription
        newTick.Value = dkpValue
        newTick.Attendees = attendees.copy()
        
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

    # def lookupCharId(self, charName:str) -> int:
    #     for key, value in self.charDict.items():
    #         if(key == charName.upper()):
    #             return value.IdCharacter

    #     charInfo: ApiCharInfo = self.oDKP.getCharacterInfo(name=charName)

    #     if(charInfo != None):
    #         self.charDict.update(charInfo.CharacterName.upper(), charInfo)
    #     else:
    #         charInfo: ApiCharInfo = self.oDKP.createCharacter(charName= charName, charRank = CharRank.Main)
    #         self.AlertMessages.append('New Character automatically added to DKP site: '+ json.dumps(newChar))
    #         self.charDict.update(charInfo.CharacterName.upper(), charInfo)
            
    #     return charInfo.IdCharacter

        
    
    

    def getLastSavePoint(self) -> ApiRaid:
        return self.__savepoint

    def exportRaidToFile(self):
        #TODO
        return
    
    def loadRaidFromFile(self, filename):
        #TODO
        return

    @property
    def AlertMessages(self)->List[str] : return self.__alertMessages