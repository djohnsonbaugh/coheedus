from unicodedata import decimal

# AttendedTicks_30: 130
# AttendedTicks_60: 259
# AttendedTicks_90: 395
# AttendedTicks_Life: 1127
# Calculated_30: 0.6372549019607843
# Calculated_60: 0.683377308707124
# Calculated_90: 0.6942003514938488
# Calculated_Life: 0.7820957668285913
# CharacterClass: "Paladin"
# CharacterName: "Althea"
# CharacterRank: "Main"
# CharacterStatus: "1"
# CurrentDKP: 64
# IdCharacter: 27005175
# TotalTicks_30: 204
# TotalTicks_60: 379
# TotalTicks_90: 569
# TotalTicks_Life: 1441

class CharRank(Enum):
    Main = 'Main'
    Box = 'Box'

class ApiCharInfo (object):

    def __init__(self):
        self.__characterName = ''
        self.__idCharacter = -1
        self.__characterRank = CharRank.Main
        self.__currentDKP = 0.0
        return

    @property
    def CharacterName(self)->str: return self.__characterName
    @property
    def IdCharacter(self)->int: return self.__idCharacter
    @property
    def CharacterRank(self)->CharRank: return self.__characterRank
    @property
    def CurrentDKP(self)->decimal: return self.__currentDKP


    @classmethod
    def from_json(cls, json_str):
        cls.__characterName:str = json_str["CharacterName"]
        cls.__idCharacter:int = json_str["IdCharacter"]
        if(json_str["CharacterRank"] == CharRank.Main):
            cls.__characterRank:CharRank =  CharRank.Main
        else:
            cls.__characterRank:CharRank =  CharRank.Box
        cls.__currentDKP:decimal = json_str["CurrentDKP"]
        return cls