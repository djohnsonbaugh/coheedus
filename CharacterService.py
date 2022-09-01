
from typing import List
from unicodedata import name

from Models.API_CharacterInfo import ApiCharInfo, CharClass, CharRank, Gender
from .openDKP import openDKP

class CharacterService (object):
    """Character Management Utility and cache"""

    def __init__(self, oDKP):
        self.__alertMessages: List[str] = List[str]
        self.oDKP : openDKP = oDKP
        self.__charDict :dict[str,ApiCharInfo] = []
        self.reload()
        

    def reload(self):
        self.__charDict.clear()
        for result in self.oDKP.getCharacters():
            self.__charDict.update(result.CharacterName, result)
        return

    def getDKP(self, name) -> int:
        return self.__charDict[name].CurrentDKP
    
    def getCharacterId(self, name) -> int:
        return self.__charDict[name].IdCharacter
        
    def updateCharacter(self, name:str, updateArgs:dict):
        charInfo = self.__charDict[name]
        for key, value in updateArgs:
            charInfo[key] = value

        charInfo = self.oDKP.updateCharacter(charInfo)
        self.__charDict.update(charInfo.CharacterName, charInfo)       
        return

    def createCharacter(self, charName:str, strRank:str, strClass:str):
        charClass = CharClass[strClass.capitalize()]
        if(charClass == None):
            charClass = CharClass.Berserker

        charRank = CharRank[strClass.capitalize()]
        if(charRank == None):
            charRank = CharRank.Main

        charInfo = self.oDKP.createCharacter(charName=charName, rank=charRank, charClass=charClass)
        self.__charDict.update(charInfo.CharacterName, charInfo)
        return

    @property
    def AlertMessages(self)->List[str] : return self.__alertMessages
