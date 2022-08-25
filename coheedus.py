from appConfig import appConfig
import eqApp
from botCommand import botCommand
import bot
from eqLog import eqLog
import regexHelper
import test
import discordbot
import time
import asyncio
import gsheets
from multiprocessing import Process, Queue

#####################################
#Read Config and Set Globals#########
#####################################
if __name__ == "__main__":
    processes:[Process] = []
    conf: appConfig = appConfig()
    GuildMessageQue:Queue = Queue()
    CommandQue:Queue = Queue()
    EQMessageQue:Queue = Queue()
    EQMessageVerificationQue:Queue = Queue()
    discordbot.init(conf, CommandQue, GuildMessageQue)
    print("Loading Config...")
    #eqApp.initConfig(conf)
    print("Config Loaded.")
#####################################

#####################################
#Processes##############################
#####################################

def processAuctioneer(conf:appConfig, CommandQue: Queue, EQMessageQue:Queue):
    bot.init(conf, CommandQue, EQMessageQue)
    bot.runAuctioneer()
    return

def processEQMessenger(conf:appConfig, EQMessageQue: Queue, EQMessageVerificationQue: Queue):
    eqApp.init(conf, EQMessageQue, EQMessageVerificationQue)
    eqApp.runEQMessagePaster()
    return

def processFileMonitor(conf:appConfig, CommandQue: Queue, GuildQue: Queue, EQMessageVerificationQue:Queue):
    log: eqLog = eqLog(conf, CommandQue, GuildQue, EQMessageVerificationQue)
    log.monitorLog()
    return

#####################################
#Main##############################
#####################################
def main():
    print("Program starting....")
    print("Log Process Starting...")
    p = Process(target=processFileMonitor,args=(conf,CommandQue, GuildMessageQue,EQMessageVerificationQue))
    p.start()
    processes.append(p)
    print("Log Process Started.")

    print("Auctioneer Process Starting...")
    p = Process(target=processAuctioneer,args=(conf,CommandQue, EQMessageQue))
    p.start()
    processes.append(p)
    print("Aunctioneer Process Started.")

    print("EQ Messenger Process Starting...")
    p = Process(target=processEQMessenger,args=(conf,EQMessageQue,EQMessageVerificationQue))
    p.start()
    processes.append(p)
    print("EQ Messenger Process Started.")

    loop = discordbot.getLoop()

    print("Tests Starting...")
    loop.create_task(test.test())
    print("Tests Started.")

    print("Guild Message Que Monitor Starting...")
    loop.create_task(discordbot.ProcessGuildMessageQue())
    print("Guild Message Que Monitor Started.")

    print("Discord Bot Starting...")
    discordbot.start()
    return

if __name__ == "__main__":
    main()