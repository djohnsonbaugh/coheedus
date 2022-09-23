from enum import Enum
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
    Visitor = 'Visitor'

class Gender(Enum):
    Male = 'Male'
    Female = 'Female'

class CharClass(Enum):
    Bard = 'Bard'
    Beastlord = 'Beastlord'
    Berserker = 'Berserker'
    Cleric = 'Cleric'
    Druid = 'Druid'
    Enchanter = 'Enchanter'
    Magician = 'Magician'
    Monk = 'Monk'
    Necromancer = 'Necromancer'
    Paladin = 'Paladin'
    Ranger = 'Ranger'
    Rogue = 'Rogue'
    ShadowKnight = 'Shadow Knight'
    Shaman = 'Shaman'
    Warrior = 'Warrior'
    Wizard = 'Wizard'

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


    
    def from_json(self, json_str):
        self.__characterName:str = json_str["CharacterName"]
        self.__idCharacter:int = json_str["IdCharacter"]
        if(json_str["CharacterRank"] == CharRank.Main):
            self.__characterRank:CharRank =  CharRank.Main
        else:
            self.__characterRank:CharRank =  CharRank.Box
        self.__currentDKP:decimal = json_str["CurrentDKP"]
        return self