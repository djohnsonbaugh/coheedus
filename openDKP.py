from urllib import response
import requests, json
from appConfig import appConfig
from enum import Enum
from pycognito import Cognito
from pycognito.utils import RequestsSrpAuth
from datetime import datetime, timedelta
import hmac
import hashlib
import boto3
import requests
from requests_aws4auth import AWS4Auth
from pycognito.aws_srp import AWSSRP
from pycognito.utils import RequestsSrpAuth
#from dotenv import load_dotenv
#load_dotenv()

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
        #self.cognitoAuthenticate()
        self.testsomethingelse()
        return

    def testsomethingelse(self):
        #THIS DID NOT WORK
        #client = boto3.client('cognito-idp', region_name="us-east-2")
        #response = client.admin_initiate_auth(
        #    UserPoolId='us-east-2_e8c5EPfnE',
        #    ClientId='2sq61k8dj39e309tnh5tm70dd4',
        #    AuthFlow='ADMIN_USER_PASSWORD_AUTH',
        #    AuthParameters={
        #        'USERNAME': self.dkpUser,
        #        'PASSWORD': self.dkpUserKey
        #    }
        #)

        #print(boto3.client('sts').get_caller_identity().get('Account'))
        #THIS WORKED 
        #client = boto3.client('cognito-idp',region_name="us-east-2")
        #aws = AWSSRP(username=self.dkpUser, password=self.dkpUserKey, pool_id='us-east-2_e8c5EPfnE',
        #client_id='2sq61k8dj39e309tnh5tm70dd4', client=client)
        #tokens = aws.authenticate_user()
        #id_token = tokens['AuthenticationResult']['IdToken']

        #self.u = Cognito('us-east-2_e8c5EPfnE','2sq61k8dj39e309tnh5tm70dd4','us-east-2', username=self.dkpUser)
        ##If this method call succeeds the instance will have the following attributes id_token, refresh_token, access_token, expires_in, expires_datetime, and token_type.
        #self.u.authenticate(password=self.dkpUserKey)  
        #id_token = self.u.access_token
        #'arn:aws:iam::714012293877:role/opendkp-admin-role'
        clientidp =  boto3.client('cognito-idp',region_name="us-east-2")
        aws = AWSSRP(username=self.dkpUser, password=self.dkpUserKey, pool_id='us-east-2_e8c5EPfnE',
        client_id='2sq61k8dj39e309tnh5tm70dd4', client=clientidp)
        tokens = aws.authenticate_user()
        id_token = tokens['AuthenticationResult']['IdToken']

        clientiden = boto3.client('cognito-identity',region_name="us-east-2")

        #no account id
        response = clientiden.get_id(
            AccountId='714012293877',
            IdentityPoolId='us-east-2:13ff4266-95dc-4a84-be2a-7b2ba75c1b83',
            Logins={'cognito-idp.us-east-2.amazonaws.com/us-east-2_e8c5EPfnE': id_token}
        )
        identity_id = response["IdentityId"] # = us-east-2:b3973271-022e-4f35-9acb-7653b65f8035

        response = clientiden.get_credentials_for_identity(
            IdentityId = identity_id,
            Logins={'cognito-idp.us-east-2.amazonaws.com/us-east-2_e8c5EPfnE': id_token}
        )
        accesskey_id = response["Credentials"]["AccessKeyId"]
        security_token = response["Credentials"]["SessionToken"]

        #not sure it worked
        #auth = RequestsSrpAuth(
        #    username=self.dkpUser,
        #    password=self.dkpUserKey,
        #    user_pool_id='us-east-2_e8c5EPfnE',
        #    client_id='2sq61k8dj39e309tnh5tm70dd4',
        #    user_pool_region='us-east-2',
        #)
        url = 'https://orgl2496uk.execute-api.us-east-2.amazonaws.com/beta/raids'
        host = "orgl2496uk.execute-api.us-east-2.amazonaws.com"
        #payload = '{"Name":"BRtestDW","Timestamp":"2022-07-31T18:35:54.300Z","Pool":{"IdPool":6,"Name":"PoP","Description":"Planes of Power","Order":4,"Raids":[]},"Ticks":[{"Description":"OnTime","Value":"0.5","RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"1945","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2000","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2015","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2030","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2045","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2100","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2115","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2130","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2145","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2200","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2215","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2230","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]}],"Items":[],"Attendance":1,"UpdatedBy":"Bigrax","UpdatedTimestamp":"2022-07-31T19:07:27.376Z"}'
        payload = json.loads('{"Name":"test2","Timestamp":"2022-08-01T05:08:33.718Z","Pool":{"IdPool":6,"Name":"PoP","Description":"Planes of Power","Order":4,"Raids":[]},"Ticks":[{"Description":"OnTime","Value":"0.5","RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"1945","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2000","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2015","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2030","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2045","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2100","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2115","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2130","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2145","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2200","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2215","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]},{"Description":"2230","Value":0.5,"RaidId":33001036,"TickId":null,"Attendees":[]}],"Items":[],"Attendance":1,"UpdatedBy":"djohnsonbaugh","UpdatedTimestamp":"2022-08-01T05:09:00.323Z"}')
        # payload = '{"IdRaid":33005777,"Pool":{"Name":"TBS","Description":"The Buried Sea","IdPool":2},"Name":"test","Timestamp":"2022-07-31T21:48:02.566Z","UpdatedBy":"Bigrax","UpdatedTimestamp":"2022-07-31T21:48:24.218Z","Attendance":1,"Ticks":[{"Description":"OnTime","Value":0.5,"RaidId":33005777,"TickId":33028736,"Attendees":[]},{"Description":"1945","Value":0.5,"RaidId":33005777,"TickId":33028737,"Attendees":[]},{"Description":"2000","Value":0.5,"RaidId":33005777,"TickId":33028738,"Attendees":[]},{"Description":"2015","Value":0.5,"RaidId":33005777,"TickId":33028739,"Attendees":[]},{"Description":"2030","Value":0.5,"RaidId":33005777,"TickId":33028740,"Attendees":[]},{"Description":"2045","Value":0.5,"RaidId":33005777,"TickId":33028741,"Attendees":[]},{"Description":"2100","Value":0.5,"RaidId":33005777,"TickId":33028742,"Attendees":[]},{"Description":"2115","Value":0.5,"RaidId":33005777,"TickId":33028743,"Attendees":[]},{"Description":"2130","Value":0.5,"RaidId":33005777,"TickId":33028744,"Attendees":[]},{"Description":"2145","Value":0.5,"RaidId":33005777,"TickId":33028745,"Attendees":[]},{"Description":"2200","Value":0.5,"RaidId":33005777,"TickId":33028746,"Attendees":[]},{"Description":"2215","Value":0.5,"RaidId":33005777,"TickId":33028747,"Attendees":[]},{"Description":"2230","Value":0.5,"RaidId":33005777,"TickId":33028748,"Attendees":[]}],"Items":[]}'
        
        #AWS4-HMAC-SHA256 Credential=ASIA2MPTS7L2USJQHIWS/20220801/us-east-2/execute-api/aws4_request, SignedHeaders=clientid;
        #cognitoinfo;
        #content-type;
        #host;
        #x-amz-date;
        #x-amz-security-token, Signature=8742f6cb9332c48523246bd31f2880037e042a78f217e69b46abc0b3ee032ae5
        curdate = datetime.now() + timedelta(hours=4)
        date = curdate.strftime('%Y%m%d')
        key = accesskey_id 
        region = "us-east-2"
        service = "execute-api"
        request = "aws4_request"

        #STEP #1 OF THE NIGHTMARE - https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
        CanonicalRequest = "PUT " + url

        credential = 'Credential='+ key + '/' + date + '/' + region +'/'+ service + '/'+ request       
        authHeaderVal = "AWS4-HMAC-SHA256 " + credential +", "
        authHeaderVal += "SignedHeaders=clientid;cognitoinfo;host;x-amz-date;, "
        firstPart = ("AWS4"+key).encode('utf-8')
        dateKey = hmac.new(firstPart, date.encode('utf-8'), hashlib.sha256).hexdigest()
        dateRegionKey = hmac.new(dateKey.encode('utf-8'), region.encode('utf-8'), hashlib.sha256).hexdigest()
        dateRegionServiceKey = hmac.new(dateRegionKey.encode('utf-8'), service.encode('utf-8'), hashlib.sha256).hexdigest()
        signingKey = hmac.new(dateRegionServiceKey.encode('utf-8'), request.encode('utf-8'), hashlib.sha256).hexdigest()

        authHeaderVal += "Signature=" + signingKey
        #AWS4-HMAC-SHA256 Credential=ASIA2MPTS7L23MAEMV6L/20220801/us-east-2/execute-api/aws4_request, SignedHeaders=clientid;cognitoinfo;host;x-amz-date;, Signature=df5fb539f8ba7ce71e9a661ff10e3f3e882954c54ae1903a36c1e679037e6509'
        datestr = curdate.strftime('%Y%m%dT%H%M%SZ')
        #x-amz-date: 20220801T061737Z 8/1/2022 2:18
        self.session.headers.update({"authorization": authHeaderVal})
        self.session.headers.update({"accept": "application/json, text/plain, */*"})
        self.session.headers.update({"cognitoinfo" : id_token})
        self.session.headers.update({"x-amz-date" : datestr})
        self.session.headers.update({"x-amz-security-token" : security_token})
        responseString = json.loads(self.session.put(url, json=payload).text)
        print(responseString)

        return

    def cognitoAuthenticate(self):
      self.u = Cognito('us-east-2_e8c5EPfnE','2sq61k8dj39e309tnh5tm70dd4','us-east-2', username=self.dkpUser)
      #If this method call succeeds the instance will have the following attributes id_token, refresh_token, access_token, expires_in, expires_datetime, and token_type.
      self.u.authenticate(password=self.dkpUserKey)  
      self.u.verify_tokens()
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


    def getDKP(self, name:str)->float:
        trashjson = json.loads(self.session.get(self.urls[oDKPURL.Summary.value]).text)["Models"]
        for row in trashjson:
            if(row["CharacterName"].lower() == name.lower()):
                return float(row["CurrentDKP"]) if row["CurrentDKP"] is not None else 10
        return 10

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
    