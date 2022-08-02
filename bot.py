import eqApp
from appConfig import appConfig
from openDKP import openDKP
from botCommand import botCommand
import regexHelper
from auctioneer import Aucitoneer
oDKP : openDKP = None
def initConfig(config: appConfig):
    global oDKP
    oDKP = openDKP(config)
    return

AdminChannel    = ""


AucMaster:Aunctioneer = Auctioneer(auctionchan = "rsay")
#obsolete....below
AuctionChannel  = "rsay"

# NORMAL COMMANDS
def exBid(cmd: botCommand) ->str:
    id          = int(cmd.regMatch.group("bidId"))      if 'bidId' in cmd.regMatch.groupdict() else -1
    item        =     cmd.regMatch.group("bidItem")     if 'bidItem' in cmd.regMatch.groupdict() else ""
    name        = cmd.Sender
    bidVal      = int(cmd.regMatch.group("bidVal"))
    bidMax      = int(cmd.regMatch.group("bidMax"))     if cmd.regMatch.group("bidMax")     is not None else bidVal
    bidInc      = int(cmd.regMatch.group("bidInc"))     if cmd.regMatch.group("bidInc")     is not None else 1
    proxyToon   =     cmd.regMatch.group("proxyToon")   if cmd.regMatch.group("proxyToon")  is not None else ""
    if id > 0:
        return "Auctions do not exist but I if they did you would have bid on auction:" + id.__str__()
    else:
        return "Auctions do not exist but I if it did you would have bid on item:" + item

def exAdmin(cmd: botCommand) -> str:
    global AdminChannel
    AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

def exDKP(cmd: botCommand) -> str:
    name        = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp         = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

# ADMIN COMMANDS
def exEditAuc(cmd: botCommand) -> str:
    id          = int(cmd.regMatch.group("aucId"))
    cmdType     = cmd.regMatch.group("cmdType")
    duration    = cmd.regMatch.group("duration")
    
    return "Auctions do not exist yet therefore i cannot " + cmdType + " them"

def exNewAuc(cmd: botCommand) -> str:
    switchOpts  = cmd.regMatch.group("switchOpts") if cmd.regMatch.group("switchOpts") is not None else ""
    itemsStr    = cmd.regMatch.group("items")
    # items = itemsStr.split(|)    
    duration    = int(cmd.regMatch.group("duration")) if cmd.regMatch.group("duration") is not None else 3
    quanity     = int(cmd.regMatch.group("quanity")) if cmd.regMatch.group("quanity") is not None else 1

    return "Can't start new auction yet on " + itemsStr + " but options would be " + switchOpts + " duration " + duration.__str__() + " quantity " + quanity.__str__()

def exChan(cmd: botCommand) -> str:
    global AuctionChannel
    AuctionChannel = cmd.Params[1] if cmd.ParCount > 0 else AuctionChannel
    return "Auction channel currently set to: " + AuctionChannel

def exClear(cmd: botCommand) -> str:
    return "Clearing something, not sure what"

def exMax(cmd: botCommand) -> str:
    numMax      = cmd.Params[1] if cmd.ParCount > 0 else 3
    return "I would set the max auctions to "+ numMax.__str__() + " if i knew how"


cmdRegistration = {
    "Normal" : {
        "ADMIN"                     : exAdmin,
        "DKP"                       : exDKP,
        regexHelper.bidWithIDPtrn   : exBid,
        regexHelper.bidWithItemPtrn : exBid
    },
    "Admin" : {
        regexHelper.aucIdCmdsPtrn   : exEditAuc,       
        regexHelper.aucCmdPtrn      : exNewAuc,       
        "CHAN"                      : exChan,
        "CLEAR"                     : exClear,
        "MAX"                       : exMax
    }
}

def reply(cmd: botCommand, message: str):
    if(cmd.Channel == "you"): eqApp.tell(cmd.Sender, message)
    else: eqApp.sendMessage(cmd.Channel, message)
    return

def execute(cmd: botCommand):
    if(cmd.Channel == AdminChannel):
        for command in cmdRegistration["Admin"]:
            if regexHelper.eqCommand(command, cmd):
                reply(cmd, cmdRegistration["Admin"][command](cmd))
                return
    for command in cmdRegistration["Normal"]:
        if regexHelper.eqCommand(command, cmd):
            reply(cmd, cmdRegistration["Normal"][command](cmd))
            return
    return

