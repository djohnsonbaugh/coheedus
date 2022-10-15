#  "Pool":{
#       "Name":"PoP",
#       "Description":"Planes of Power",
#       "IdPool":6
#    },
import json


class ApiRaidPool(object):

    def __init__(self):
        self.Name = "PoP"
        self.Description = "Planes of Power"
        self.IdPool = 6
        return
    
    #PROPERTIES
    # @property
    # def Name(self)->int: return self.Name
    # @property
    # def Description(self)->str: return self.Description
    # @property
    # def IdPool(self)->int: return self.IdPool


    def from_json(self, json_str):
        self.Name:str = json_str["Name"]
        self.Description:str = json_str["Description"]
        self.IdPool:int = json_str["IdPool"]
        return self
        
    # def toJson(self) -> str:
    #     #FIXME
    #     # return '{"Name":"' + self.Name + '","Description:"'+self.Description +"',IdPool:" + self.IdPool+"}"
    #     return json.dumps(self)
        