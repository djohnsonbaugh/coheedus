from urllib import response
import requests, json
from Models.API_CharacterInfo import ApiCharInfo
from Models.API_Raid import ApiRaid
from Models.API_RaidTemplate import ApiRaidTemplate
from appConfig import appConfig
from enum import Enum
import hmac
import hashlib
import boto3
import requests
from pycognito.aws_srp import AWSSRP
from datetime import datetime


class oDKPURL(Enum):
    Summary = 0

class openDKP(object):
    """description of class"""
    def __init__(self, conf:appConfig):
        self.clientID = conf.get("OPENDKP","clientid","") 
        # self.urls :[str] = []
        self.raidTemplateName = conf.get("OPENDKP","raidtemplate","") 
        #for url in oDKPURL:
        #    self.urls.append(conf.get("OPENDKPAPIURLS",url.name,""))
        self.session = None
        self.createNewSession()
        #self.loadRaidTemplate2()
        return

    def createAdjustment4(self):
        method = 'PUT'
        url = 'https://5koqnuxrt7.execute-api.us-east-2.amazonaws.com/beta/adjustments'
        host = "5koqnuxrt7.execute-api.us-east-2.amazonaws.com"
        payload='{"Character": "Tinyrax","Name": "API Testibng","Description": "Additional Details if needed","Value": 1,"Timestamp": "8/7/2022"}'
        conPath = '/beta/adjustments'
        conQuery = ''
        contentType = "application/json; charset=UTF-8"
        

        curdate = datetime.utcnow()
        datestr = curdate.strftime('%Y%m%dT%H%M%SZ')
        clientidp =  boto3.client('cognito-idp',region_name="us-east-2")
        aws = AWSSRP(username=self.dkpUser, password=self.dkpUserKey, pool_id='us-east-2_e8c5EPfnE',
        client_id='2sq61k8dj39e309tnh5tm70dd4', client=clientidp)
        tokens = aws.authenticate_user()
        id_token = tokens['AuthenticationResult']['IdToken']       
        clientiden = boto3.client('cognito-identity',region_name="us-east-2")
        #no account id
        response1 = clientiden.get_id(
            AccountId='714012293877', 
            IdentityPoolId='us-east-2:13ff4266-95dc-4a84-be2a-7b2ba75c1b83',
            Logins={'cognito-idp.us-east-2.amazonaws.com/us-east-2_e8c5EPfnE': id_token}
        ) 
        identity_id = response1["IdentityId"]
        response2 = clientiden.get_credentials_for_identity(
            IdentityId = identity_id,
            Logins={'cognito-idp.us-east-2.amazonaws.com/us-east-2_e8c5EPfnE': id_token}
        )
        accesskey_id = response2["Credentials"]["AccessKeyId"]
        security_token = response2["Credentials"]["SessionToken"]
        realsecretkey = response2["Credentials"]["SecretKey"]
        
    
# Auth value from webpage: 
# AWS4-HMAC-SHA256 
# Credential=ASIA2MPTS7L2WQI6GQCH/20220807/us-east-2/execute-api/aws4_request, 
# SignedHeaders=clientid;cognitoinfo;content-type;host;x-amz-date;x-amz-security-token, 
# Signature=3baeb16e933dd980dc19e1ee0e6c0252347a8dcc034cfa7de7abbc9462929279
        signedHeadersDic = {"clientid": self.clientID, "cognitoinfo" : id_token, "content-type": contentType,"host": host, "x-amz-date":datestr, "x-amz-security-token":security_token}
        self.session.headers.update({"accept": "application/json, text/plain, */*"})
        self.session.headers.update({"content-type": contentType})
        self.session.headers.update({"cognitoinfo" : id_token})
        self.session.headers.update({"x-amz-date" : datestr})
        self.session.headers.update({"x-amz-security-token" : security_token})
        self.session.headers.update({"clientid" : self.clientID})
        self.session.headers.update({"content-length" : payload.__len__().__str__()})


        # req = requests.Request(method=method, url=url, json=payload, headers=self.session.headers)
        # reqBody = json.dumps(req.json)
        # if not isinstance(reqBody, bytes):
        #         reqBody = reqBody.encode("utf-8")
        # self.session.headers.update({"authorization": getAuthValue(method, conPath, conQuery, accesskey_id, signedHeadersDic, payload)})
        self.session.headers.update({"authorization": getAuthValue(method=method, canUri=conPath,canQueryString=conQuery,secretKey=realsecretkey, accessKey=accesskey_id, signedHeaders=signedHeadersDic, payload=payload)})
        # self.session.headers.update({"authorization": getAuthValue(method, conPath, conQuery, accesskey_id, signedHeadersDic, reqBody)})
        # req.headers = self.session.headers
        # prepReq = req.prepare()
        # response = self.session.send(prepReq)
        response =  self.session.request(method=method, url=url, data=payload)
        print(response.text)
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
        return 10

    def getCharacterInfo(self, name:str) -> ApiCharInfo:
        trashjson = json.loads(self.session.get(self.urls[oDKPURL.Summary.value]).text)["Models"]
        for row in trashjson:
            if(row["CharacterName"] == name):
                return ApiCharInfo.from_json(row)
        return

    def loadRaidTemplate(self):
        url = "https://4jmtrkwc86.execute-api.us-east-2.amazonaws.com/beta/admin/settings/raid_templates"

        responseString = json.loads(self.session.get(url).text)["SettingValue"]
      
        jsonTemplates = json.loads(responseString)["Templates"]
        for row in jsonTemplates:
            if(row["Name"] == self.raidTemplateName):
                return row
        return


    def loadRaidTemplate2(self) -> ApiRaidTemplate:
        url = "https://4jmtrkwc86.execute-api.us-east-2.amazonaws.com/beta/admin/settings/raid_templates"

        responseString = json.loads(self.session.get(url).text)["SettingValue"]
      
        jsonTemplates = json.loads(responseString)["Templates"]
        for row in jsonTemplates:
            if(row["Name"] == self.raidTemplateName):
                template = ApiRaidTemplate.from_json(row)
                return template
        return

    def pushRaid(raid:ApiRaid):

        return


    # Item Lookup
    #https://72rv4f6y1f.execute-api.us-east-2.amazonaws.com/beta/items/autocomplete?item=Helm of flowing&limit=5&game=0
    # Returns "ItemName":"Blade of War","ItemID":25989,"GameItemId":25989}
    def lookupItem(self, itemName:str):
        url = "https://72rv4f6y1f.execute-api.us-east-2.amazonaws.com/beta/items/autocomplete?item=" + itemName + "&limit=5&game=0"

        responseItems = json.loads(self.session.get(url).text)
        for row in responseItems:
            return row
        return
        

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


# x-amz-date signed header is expected
def getAuthValue( method, canUri, canQueryString, secretKey, accessKey, signedHeaders: dict, payload: str):
    algorithm = 'AWS4-HMAC-SHA256'
    region = "us-east-2"
    service = "execute-api"
    
    canonical_headers = ''
    signed_headers = ''
    dateStamp = datetime.utcnow().strftime('%Y%m%d')

    for key, value in signedHeaders.items():
        canonical_headers += key + ':' + value + '\n'
        if(signed_headers.__len__() > 1 ):
            signed_headers += ';' + key 
        else:
            signed_headers += key
    
    reqBody = payload
    if not isinstance(reqBody, bytes):
                reqBody = reqBody.encode("utf-8")

    # ************* TASK 1: CREATE A CANONICAL REQUEST *************
    payload_hash = hashlib.sha256(reqBody).hexdigest()
    canonical_request = method + '\n' + canUri + '\n' + canQueryString + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    # canonical_request = method + '\n' + canUri + '\n' + canQueryString + '\n' + canonical_headers + '\n' + signed_headers + '\n' 
    print(canonical_request.encode('utf-8'))
    # ************* TASK 2: CREATE THE STRING TO SIGN*************
    # Match the algorithm to the hashing algorithm you use, either SHA-1 or
    # SHA-256 (recommended)
    credential_scope = dateStamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  signedHeaders['x-amz-date'] + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    print(string_to_sign.encode('utf-8'))
    # ************* TASK 3: CALCULATE THE SIGNATURE *************
    # Create the signing key using the function defined above.
    signing_key = getSignatureKey(secretKey, dateStamp, region, service)
    # Sign the string_to_sign using the signing_key
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
    # Put the signature information in a header named Authorization.
    return algorithm + ' ' + 'Credential=' + accessKey + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

