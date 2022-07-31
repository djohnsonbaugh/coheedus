import eqApp
from appConfig import appConfig
from openDKP import openDKP
from botCommand import botCommand
import regexHelper
oDKP : openDKP = None
def initConfig(config: appConfig):
    global oDKP
    oDKP = openDKP(config)
    return

AdminChannel = ""
AuctionChannel = "rsay"

# NORMAL COMMANDS
def exAucID(cmd: botCommand) ->str:

    return "Not Implemented but i found and id:" + cmd.regMatch.group(1)

def exAdmin(cmd: botCommand) -> str:
    global AdminChannel
    AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

def exDKP(cmd: botCommand) -> str:
    name = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

# ADMIN COMMANDS
def exAuc(cmd: botCommand) -> str:
    return "Not Implemented"

def exChan(cmd: botCommand) -> str:
    global AuctionChannel
    if(cmd.ParCount > 0):
        AuctionChannel = cmd.Params[1]
    return "Auction channel currently set to: " + AuctionChannel


cmdRegistration = {
    "Normal" : {
        "ADMIN"                     : exAdmin,
        "DKP"                       : exDKP,
        regexHelper.aucIDPattern    : exAucID
    },
    "Admin" : {
        "AUC"                       : exAuc,       
        "CHAN"                      : exChan,       
    }
}

def reply(cmd: botCommand, message: str):
    if(cmd.Channel == "you"): eqApp.tell(cmd.Sender, message)
    else: eqApp.sendMessage(cmd.Channel, message)
    return

def execute(cmd: botCommand):
    for command in cmdRegistration["Normal"]:
        if regexHelper.eqCommand(command, cmd):
            reply(cmd, cmdRegistration["Normal"][command](cmd))
            return
    if(cmd.Channel == AdminChannel):
        for command in cmdRegistration["Admin"]:
            if regexHelper.eqCommand(command, cmd):
                reply(cmd, cmdRegistration["Admin"][command](cmd))
                return
    return

