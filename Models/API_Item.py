from unicodedata import decimal


# {
#          "CharacterName":"Althea",
#          "IdCharacter":27005175,
#          "ItemName":"Yar`Lir's Fang",
#          "ItemID":57200,
#          "GameItemId":57200,
#          "DkpValue":2.0,
#          "Notes":""
#       },

class ApiItem (object):

    def __init__(self):
        self.__characterName = ""
        self.__idCharacter = -1
        self.__itemName = ""
        self.__itemId = -1
        self.__gameItemId = -1
        self.__dkpValue = 0.0
        self.__notes = ""
        return

    #PROPERTIES
    @property
    def CharacterName(self)->str: return self.__characterName
    @property
    def IdCharacter(self)->int: return self.__idCharacter
    @property
    def ItemName(self)-> str: return self.__itemName
    @property
    def ItemID(self)->int: return self.__itemId
    @property
    def GameItemId(self)->int: return self.__gameItemId
    @property
    def DkpValue(self)->decimal: return self.__dkpValue
    @property
    def Notes(self)-> str: return self.__notes

    

