import eqApp
from appConfig import appConfig
from openDKP import openDKP
from botCommand import botCommand
import regexHelper
oDKP : openDKP = None
def initConfig(config: appConfig):
    global oDKP
    oDKP = openDKP(config)
    oDKP.insertRaid()
    return

AdminChannel = ""
AuctionChannel = "rsay"

# NORMAL COMMANDS
def exBid(cmd: botCommand) ->str:
    id = cmd.regMatch.group("bidId") if 'bidId' in cmd.regMatch.groupdict() else -1
    item = cmd.regMatch.group("bidItem") if 'bidItem' in cmd.regMatch.groupdict() else ""
    bidVal = cmd.regMatch.group("bidVal")
    bidMax = cmd.regMatch.group("bidMax")
    bidInc = cmd.regMatch.group("bidInc")
    proxyToon = cmd.regMatch.group("proxyToon")
    if id > 0:
        return "Not Implemented but I if it did you would have bid on auction:" + id
    else:
        return "Not Implemented but I if it did you would have bid on item:" + item

def exAdmin(cmd: botCommand) -> str:
    global AdminChannel
    AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

def exDKP(cmd: botCommand) -> str:
    name = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

# ADMIN COMMANDS
def exEditAuc(cmd: botCommand) -> str:
    id = cmd.regMatch.group("aucId")
    cmdType = cmd.regMatch.group("cmdType")
    duration = cmd.regMatch.group("duration")
    
    return "Auctions do not exist yet therefore i cannot " + cmdType + " them"

def exNewAuc(cmd: botCommand) -> str:
    switchOpts = cmd.regMatch.group("switchOpts")
    itemsStr = cmd.regMatch.group("items")
    # items = itemsStr.split(|)    
    duration = cmd.regMatch.group("duration")
    quanity = cmd.regMatch.group("quanity")

    return "Can't start new auction yet on " + itemsStr + " but options would be " + switchOpts + " duration " + duration + " quantity " + quanity

def exChan(cmd: botCommand) -> str:
    global AuctionChannel
    if(cmd.ParCount > 0):
        AuctionChannel = cmd.Params[1]
    return "Auction channel currently set to: " + AuctionChannel


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

