#  "Pool":{
#       "Name":"PoP",
#       "Description":"Planes of Power",
#       "IdPool":6
#    },
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