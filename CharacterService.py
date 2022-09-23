
from typing import List
from unicodedata import name

from Models.API_CharacterInfo import ApiCharInfo, CharClass, CharRank, Gender
from appConfig import appConfig
from openDKP import openDKP

class CharacterService (object):
    """Character Management Utility and cache"""

    def __init__(self):
        conf: appConfig = appConfig()
        self.__alertMessages: List[str] = List[str]
        self.oDKP : openDKP = openDKP(conf)
        self.__charDict :dict[str,ApiCharInfo] = dict()
        self.reload()
        

    def reload(self):
        self.__charDict.clear()
        for result in self.oDKP.getCharacters():
            self.__charDict[result.CharacterName] =  result
        return

    def isMain(self, charName:str) -> bool:
        return self.__charDict[charName].CharacterRank == CharRank.Main

    def getDKP(self, name:str) -> int:
        return self.__charDict[name].CurrentDKP
    
    def getCharacterId(self, name:str) -> int:
        return self.__charDict[name].IdCharacter
        
    def updateCharacter(self, name:str, updateArgs:dict):
        charInfo:ApiCharInfo = self.__charDict[name]
        for key, value in updateArgs:
            charInfo[key] = value

        charInfo = self.oDKP.updateCharacter(charInfo)
        self.__charDict.update(charInfo.CharacterName, charInfo)       
        return

    def createCharacter(self, charName:str, strRank:str, strClass:str):
        charClass = CharClass[strClass]
        if(charClass == None):
            charClass = CharClass.Berserker

        charRank = CharRank[strRank]
        if(charRank == None):
            charRank = CharRank.Main

        charInfo: ApiCharInfo = self.oDKP.createCharacter(charName=charName, rank=charRank, charClass=charClass)
        self.__charDict.update(charInfo.CharacterName, charInfo)
        return

    @property
    def AlertMessages(self)->List[str] : return self.__alertMessages
