import bot
from openDKP import openDKP
import eqApp
from appConfig import appConfig
import asyncio

oDKP: openDKP = None

async def test():
    global oDKP
    oDKP = bot.oDKP
    
    #TEST Single Calls HERE
    #######################
    oDKP.insertRaid()
    #print("Bigrax DKP is " + oDKP.getDKP("Bigrax").__str__())

    while True:
        #TEST Repetetive Calls Here
        ###########################
        
        #print(eqApp.isEQActive())
        
        await asyncio.sleep(5)
