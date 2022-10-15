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
    def __init__(self):
        return

    def populate(self,  description, value, raidId, tickId, attendees):
        self.Description:str = description
        self.Value:decimal = value
        self.RaidId:int = raidId
        self.TickId:int = tickId
        self.Attendees:List[str] = attendees
        return

    # @property
    # def Description(self)->str: return self.Description
    # @property
    # def Value(self)->decimal: return self.Value
    # @property
    # def RaidId(self)->int: return self.RaidId
    # @property
    # def TickId(self)->int: return self.TickId
    # @property
    # def Attendees(self)->List[str]: return self.Attendees
    
    def from_json(self, json_str):
        self.Description:str = json_str["Description"]
        self.Value:decimal = json_str["Value"]
        self.RaidId:int = json_str["RaidId"]
        self.TickId:int = json_str["TickId"]
        self.Attendees:List[str] = json_str["Attendees"]
        return self
    
    def toJson(self) -> str:
        return json.dumps(self)