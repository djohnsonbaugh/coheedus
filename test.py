import bot
from openDKP import openDKP
import eqApp
from appConfig import appConfig
import asyncio
import amz
oDKP: openDKP = None

async def test():
    global oDKP
    oDKP = bot.oDKP

    #TEST Single Calls HERE
    #######################
    #amz.postStuff()
    #print("Bigrax DKP is " + oDKP.getDKP("Bigrax").__str__())
    print("test would have run..")

    while True:
        #TEST Repetetive Calls Here
        ###########################
        
        #print(eqApp.isEQActive())
        
        await asyncio.sleep(5)
