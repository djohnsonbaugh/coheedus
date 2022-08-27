import json
from typing import List
from unicodedata import decimal


# {
#          "Description":"2030",
#          "Value":0.5,
#          "RaidId":33006461,
#          "TickId":33032277,
#          "Attendees":[
#             "Althea",
#             "Bigrax",
#             "Cookar",
#             "Dethas",
#             "Dwendrox",
#             "Gravestones",
#             "Itassha",
#             "Khyn",
#             "Matron",
#             "Procto",
#             "Sarcasmo",
#             "Tebe",
#             "Tenten",
#             "Tomwandry",
#             "Vanishing",
#             "Warrden",
#             "Wraith",
#             "Xathrid",
#             "Zaaxi"
#          ]
#       },

class ApiRaidTick (object): 
    def __init__(self, description, value, raidId, tickId, attendees):
        self.__description:str = description
        self.__value:decimal = value
        self.__raidId:int = raidId
        self.__tickId:int = tickId
        self.__attendees:List[str] = attendees
        return

    @property
    def Description(self)->str: return self.__description
    @property
    def Value(self)->decimal: return self.__value
    @property
    def RaidId(self)->int: return self.__raidId
    @property
    def TickId(self)->int: return self.__tickId
    @property
    def Attendees(self)->List[str]: return self.__attendees
    
    @classmethod
    def from_json(cls, json_str):
        cls.__description:str = json_str["Description"]
        cls.__value:decimal = json_str["Value"]
        cls.__raidId:int = json_str["RaidId"]
        cls.__tickId:int = json_str["TickId"]
        cls.__attendees:List[str] = json_str["Attendees"]
        return cls