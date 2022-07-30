import time
from datetime import datetime
import os
from time import sleep
from enum import Enum
import winOS
import eqApp
from eqLog import eqLog
from appConfig import appConfig
import asyncio
import concurrent.futures
import regexHelper
from bot import botCommand
from openDKP import openDKP

#####################################
#Read Config and Set Globals#########
#####################################
print("Loading Config...")

conf: appConfig = appConfig()
eqApp.initConfig(conf)
log: eqLog = eqLog(conf)
oDKP : openDKP = openDKP(conf)


print("Config Loaded.")
#####################################


async def fakeloop():
    while True:
        print(winOS.getActiveWindow())
        for i in range(0,50):
            await asyncio.sleep(0)
            time.sleep(.1)

    return

def eventNewLogLine(line:str):
    cmd : botCommand = botCommand()
    if regexHelper.isCommand(line, cmd):
        print("command detected")
    else:
        print(line, end='')

async def main():
    print("Bigrax's DKP is " + oDKP.getDKP("Bigrax").__str__() + ".")
    print("Program starting....")
    loop = asyncio.get_running_loop()

    loop.create_task(fakeloop())
    print("Monitoring Starting....")
    loop.create_task(log.monitorLog(eventNewLogLine))
    print("Monitoring Started.")
    
    while True:
        await asyncio.sleep(0)
    return

asyncio.run(main())
