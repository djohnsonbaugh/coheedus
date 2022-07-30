import requests, json
from appConfig import appConfig

class openDKP(object):
    """description of class"""
    def __init__(self, conf:appConfig):
        self.clientID = conf.get("OPENDKP","clientid","")
        self.server = conf.get("OPENDKPAPIURLS","summary","")
        self.session = None
        createNewSession()
        return

    def createNewSession(self):
        self.session = requests.Session()
        self.session.headers.update({"clientid":self.clientID})


    def getDKP(self):

        return
