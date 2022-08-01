from urllib import response
import requests, json
from appConfig import appConfig
from enum import Enum
from pycognito import Cognito
from pycognito.utils import RequestsSrpAuth
from datetime import datetime
import hmac
import hashlib

class oDKPURL(Enum):
    Summary = 0

class openDKP(object):
    """description of class"""
    def __init__(self, conf:appConfig):
        self.clientID = conf.get("OPENDKP","clientid","") 
        self.userPoolId = conf.get("OPENDKP","userpoolid","") 
        self.dkpUser = conf.get("OPENDKP","dkpuser","") 
        self.dkpUserKey = conf.get("OPENDKP","dkpuserkey","") 
        self.urls :[str] = []
        self.raidTemplateName = conf.get("OPENDKP","raidtemplate","") 
        for url in oDKPURL:
            self.urls.append(conf.get("OPENDKPAPIURLS",url.name,""))
        self.session = None
        self.createNewSession()
        self.cognitoAuthenticate()

        return

    def cognitoAuthenticate(self):
      self.u = Cognito('us-east-2_e8c5EPfnE','2sq61k8dj39e309tnh5tm70dd4', username=self.dkpUser)
      self.u.authenticate(password=self.dkpUserKey)  
      self.checkTokens()

    def checkTokens(self):
        self.u.check_token()

        curTime = datetime.now()
        date = curTime.strftime('%Y-%m-%d')
        key = "ASIA2MPTS7L23MAEMV6L" 
        region = "us-east-2"
        service = "execute-api"
        request = "aws4_request"

        credential = 'Credential='+ key + '/' + date + '/' + region +'/'+ service + '/'+ request       

        authHeaderVal = "AWS4-HMAC-SHA256 " + credential +", "
        authHeaderVal += "SignedHeaders=clientid;cognitoinfo;host;x-amz-date;, "
        firstPart = ("AWS4"+key).encode('utf-8')
        dateKey = hmac.new(firstPart, date.encode('utf-8'), hashlib.sha256).hexdigest()
        dateRegionKey = hmac.new(dateKey.encode('utf-8'), region.encode('utf-8'), hashlib.sha256).hexdigest()
        dateRegionServiceKey = hmac.new(dateRegionKey.encode('utf-8'), service.encode('utf-8'), hashlib.sha256).hexdigest()
        signingKey = hmac.new(dateRegionServiceKey.encode('utf-8'), request.encode('utf-8'), hashlib.sha256).hexdigest()

        authHeaderVal += "Signature=" + signingKey
        self.session.headers.update({"authorization": authHeaderVal})
        self.session.headers.update({"cognitoinfo" : self.u.access_token})
        self.session.headers.update({"x-amz-date" : curTime.strftime('%Y-%m-%dT%H:%M:%S.%f%z') })

            

    def createNewSession(self):
        self.session = requests.Session()
        self.session.headers.update({"clientid":self.clientID})
        return


    def getDKP(self, name:str):
        trashjson = json.loads(self.session.get(self.urls[oDKPURL.Summary.value]).text)["Models"]
        for row in trashjson:
            if(row["CharacterName"].lower() == name.lower()):
                return row["CurrentDKP"]
        return

    def loadRaidTemplate(self):
        url = "https://4jmtrkwc86.execute-api.us-east-2.amazonaws.com/beta/admin/settings/raid_templates"

        responseString = json.loads(self.session.get(url).text)["SettingValue"]
      
        jsonTemplates = json.loads(responseString)["Templates"]
        for row in jsonTemplates:
            if(row["Name"] == self.raidTemplateName):
                return row
        return

    def insertRaid(self):
        self.checkTokens()
        url = 'https://orgl2496uk.execute-api.us-east-2.amazonaws.com/beta/raids'
        payload = '{"Name":"BRtest","Timestamp":"2022-07-31T18:35:54.300Z","Pool":{"IdPool":6,"Name":"PoP","Description":"Planes of Power","Order":4,"Raids":[]},"Ticks":[{"Description":"OnTime","Value":"0.5","RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"1945","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2000","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2015","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2030","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2045","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2100","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2115","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2130","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2145","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2200","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2215","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2230","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]}],"Items":[],"Attendance":1,"UpdatedBy":"Bigrax","UpdatedTimestamp":"2022-07-31T19:07:27.376Z"}'
        # payload = '{"IdRaid":33005777,"Pool":{"Name":"TBS","Description":"The Buried Sea","IdPool":2},"Name":"test","Timestamp":"2022-07-31T21:48:02.566Z","UpdatedBy":"Bigrax","UpdatedTimestamp":"2022-07-31T21:48:24.218Z","Attendance":1,"Ticks":[{"Description":"OnTime","Value":0.5,"RaidId":33005777,"TickId":33028736,"Attendees":[]},{"Description":"1945","Value":0.5,"RaidId":33005777,"TickId":33028737,"Attendees":[]},{"Description":"2000","Value":0.5,"RaidId":33005777,"TickId":33028738,"Attendees":[]},{"Description":"2015","Value":0.5,"RaidId":33005777,"TickId":33028739,"Attendees":[]},{"Description":"2030","Value":0.5,"RaidId":33005777,"TickId":33028740,"Attendees":[]},{"Description":"2045","Value":0.5,"RaidId":33005777,"TickId":33028741,"Attendees":[]},{"Description":"2100","Value":0.5,"RaidId":33005777,"TickId":33028742,"Attendees":[]},{"Description":"2115","Value":0.5,"RaidId":33005777,"TickId":33028743,"Attendees":[]},{"Description":"2130","Value":0.5,"RaidId":33005777,"TickId":33028744,"Attendees":[]},{"Description":"2145","Value":0.5,"RaidId":33005777,"TickId":33028745,"Attendees":[]},{"Description":"2200","Value":0.5,"RaidId":33005777,"TickId":33028746,"Attendees":[]},{"Description":"2215","Value":0.5,"RaidId":33005777,"TickId":33028747,"Attendees":[]},{"Description":"2230","Value":0.5,"RaidId":33005777,"TickId":33028748,"Attendees":[]}],"Items":[]}'
        responseString = json.loads(self.session.put(url, payload).text)
        print(responseString)
      



# Item Lookup
#https://72rv4f6y1f.execute-api.us-east-2.amazonaws.com/beta/items/autocomplete?item=Helm of flowing&limit=5&game=0
    