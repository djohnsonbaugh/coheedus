from appConfig import appConfig
import eqApp
from botCommand import botCommand
import bot
from eqLog import eqLog
import regexHelper
import test
import discordbot

#####################################
#Events##############################
#####################################
async def eventNewLogLine(line:str):
    cmd : botCommand = botCommand()
    if regexHelper.isCommand(line, cmd):
        bot.execute(cmd)
    elif regexHelper.isGuildMessage(line, cmd):
        await discordbot.newGuildMessageEvent(cmd.Sender, cmd.Text)
    else:
        print(line, end='')

def eventNewDiscordMessage(sender:str, line:str):
    cmd : botCommand = botCommand()
    cmd.set(sender, "discord", line)
    bot.execute(cmd)
    return

#####################################
#Read Config and Set Globals#########
#####################################
print("Loading Config...")

conf: appConfig = appConfig()
eqApp.initConfig(conf)
bot.init(conf, discordbot.botReply)
log: eqLog = eqLog(conf)
discordbot.init(conf, eventNewDiscordMessage)
print("Config Loaded.")
#####################################

#####################################
#Main##############################
#####################################
def main():
    print("Program starting....")

    #Have to use the discord internal discord asyncio loop instead of our own
    loop = discordbot.getLoop()

    print("Tests Starting...")
    loop.create_task(test.test())
    print("Tests Started.")

    print("Monitoring Starting....")
    loop.create_task(log.monitorLog(eventNewLogLine))
    print("Monitoring Started.")

    print("Auctioneer Starting....")
    loop.create_task(bot.runAuctioneer())
    print("Auctioneer Started.")

    print("Discord Bot Starting...")
    discordbot.start()
    
    return

main()