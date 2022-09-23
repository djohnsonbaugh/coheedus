from CharacterService import CharacterService
from RaidService import RaidService
import bot
from openDKP import openDKP
import eqApp
from appConfig import appConfig
import asyncio
oDKP: openDKP = None

async def test():
    global oDKP
    #oDKP = bot.oDKP
    raidService: RaidService = RaidService()
    charService: CharacterService = CharacterService()

    #TEST Single Calls HERE
    #######################
    #amz.postStuff()
    #print("Bigrax DKP is " + oDKP.getDKP("Bigrax").__str__())
    
    #33006767
    raidId :int = raidService.loadRaid(33006767)
    print("Loading old raid. Returned: "+  str(raidId) )

    print("Bigrax DKP is " + str(charService.getDKP("Bigrax")) )

    print("test would have run..")

    while True:
        #TEST Repetetive Calls Here
        ###########################
        
        #print(eqApp.isEQActive())
        
        await asyncio.sleep(5)
