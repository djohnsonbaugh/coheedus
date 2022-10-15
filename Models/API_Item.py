import json
from unicodedata import decimal


# {
#          "CharacterName":"Althea",
#          "IdCharacter":27005175,
#          "ItemName":"Yar`Lir's Fang",
#          "ItemID":57200,
#          "ItemID":57200,
#          "DkpValue":2.0,
#          "Notes":""
#       },

class ApiItem (object):

    def __init__(self):
        self.CharacterName = ""
        self.IdCharacter = -1
        self.ItemName = ""
        self.ItemID = -1
        self.ItemID = -1
        self.DkpValue = 0.0
        self.Notes = ""
        return

    def populate(self, charName: str, idChar:int, itemName: str, itemId:int, gameItemId:int, dkpValue:decimal, notes:str) -> None:
        self.CharacterName = charName
        self.IdCharacter = idChar
        self.ItemName = itemName
        self.ItemId = itemId
        self.GameItemId = gameItemId
        self.DkpValue = dkpValue
        self.Notes = notes
        return
    #PROPERTIES
    # @property
    # def CharacterName(self)->str: return self.CharacterName
    # @CharacterName.setter
    # def CharacterName(self, charName:str)-> None: self.CharacterName=charName
    # @property
    # def IdCharacter(self)->int: return self.IdCharacter
    # @IdCharacter.setter
    # def IdCharacter(self, idChar:int)-> None: self.IdCharacter=idChar
    # @property
    # def ItemName(self)-> str: return self.__itemName
    # @property
    # def ItemID(self)->int: return self.__itemId
    # @property
    # def ItemID(self)->int: return self.__gameItemId
    # @property
    # def DkpValue(self)->decimal: return self.__dkpValue
    # @property
    # def Notes(self)-> str: return self.__notes

    
    
    def from_json(self, json_str):
        self.CharacterName = json_str["CharacterName"]
        self.IdCharacter = json_str["IdCharacter"]
        self.ItemName = json_str["ItemName"]
        self.ItemID = json_str["ItemID"]
        self.GameItemId = json_str["GameItemId"]
        self.DkpValue = json_str["DkpValue"]
        self.Notes = json_str["Notes"]
        return self
    
    # def toJson(self) -> str:
    #     return json.dumps(self)
