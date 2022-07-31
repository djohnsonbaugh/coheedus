import asyncio
from appConfig import appConfig
import eqApp
from botCommand import botCommand
import bot
from eqLog import eqLog
import regexHelper
import test

#####################################
#Read Config and Set Globals#########
#####################################
print("Loading Config...")

conf: appConfig = appConfig()
eqApp.initConfig(conf)
bot.initConfig(conf)
log: eqLog = eqLog(conf)

print("Config Loaded.")
#####################################

#####################################
#Events##############################
#####################################
def eventNewLogLine(line:str):
    cmd : botCommand = botCommand()
    if regexHelper.isCommand(line, cmd):
        bot.execute(cmd)
    else:
        print(line, end='')

#####################################
#Main##############################
#####################################

async def main():
    print("Program starting....")
    loop = asyncio.get_running_loop()

    print("Tests Starting...")
    loop.create_task(test.test())
    print("Tests Started.")

    print("Monitoring Starting....")
    loop.create_task(log.monitorLog(eventNewLogLine))
    print("Monitoring Started.")
    
    while True:
        await asyncio.sleep(0)
    return

asyncio.run(main())
