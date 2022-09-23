#  "Pool":{
#       "Name":"PoP",
#       "Description":"Planes of Power",
#       "IdPool":6
#    },
import json


class ApiRaidPool(object):

    def __init__(self):
        self.__name = "PoP"
        self.__description = "Planes of Power"
        self.__idPool = 6
        return
    
    #PROPERTIES
    @property
    def Name(self)->int: return self.__name
    @property
    def Description(self)->str: return self.__description
    @property
    def IdPool(self)->int: return self.__idPool


    def from_json(self, json_str):
        self.__name:str = json_str["Name"]
        self.__description:str = json_str["Description"]
        self.__idPool:int = json_str["IdPool"]
        return self
        
    def toJson(self) -> str:
        # return '{"Name":"' + self.__name + '","Description:"'+self.__description +"',IdPool:" + self.__idPool+"}"
        return json.dumps(self)
        