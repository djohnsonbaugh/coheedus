from urllib import response
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
        self.raidTemplateName = conf.get("OPENDKP","raidtemplate","") 
        for url in oDKPURL:
            self.urls.append(conf.get("OPENDKPAPIURLS",url.name,""))
        self.session = None
        self.createNewSession()
        return



    def createNewSession(self):
        self.session = requests.Session()
        self.session.headers.update({"clientid":self.clientID})
        return


    def getDKP(self, name:str)->float:
        trashjson = json.loads(self.session.get(self.urls[oDKPURL.Summary.value]).text)["Models"]
        for row in trashjson:
            if(row["CharacterName"].lower() == name.lower()):
                return float(row["CurrentDKP"]) if row["CurrentDKP"].isnumeric() else 10
        return 10

    def loadRaidTemplate(self):
        url = "https://4jmtrkwc86.execute-api.us-east-2.amazonaws.com/beta/admin/settings/raid_templates"

        responseString = json.loads(self.session.get(url).text)["SettingValue"]
      
        jsonTemplates = json.loads(responseString)["Templates"]
        for row in jsonTemplates:
            if(row["Name"] == self.raidTemplateName):
                return row
        return




# Item Lookup
#https://72rv4f6y1f.execute-api.us-east-2.amazonaws.com/beta/items/autocomplete?item=Helm of flowing&limit=5&game=0
    