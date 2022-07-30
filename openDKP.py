import requests, json
from appConfig import appConfig
from enum import Enum
class oDKPURL(Enum):
    Summary = 0

class openDKP(object):
    """description of class"""
    def __init__(self, conf:appConfig):
        self.clientID = conf.get("OPENDKP","clientid","")
        self.urls :[str] = []
        for url in oDKPURL:
            self.urls.append(conf.get("OPENDKPAPIURLS",url.name,""))
        self.session = None
        self.createNewSession()
        return



    def createNewSession(self):
        self.session = requests.Session()
        self.session.headers.update({"clientid":self.clientID})
        return


    def getDKP(self, name:str):
        trashjson = json.loads(self.session.get(self.urls[oDKPURL.Summary.value]).text)["Models"]
        for row in trashjson:
            if(row["CharacterName"] == name):
                return row["CurrentDKP"]
        return
