import eqApp
from appConfig import appConfig
from openDKP import openDKP
from botCommand import botCommand
import regexHelper
from auctioneer import Auctioneer
import asyncio
import re
oDKP : openDKP = None
def initConfig(config: appConfig):
    global oDKP
    oDKP = openDKP(config)
    return

BotDebug:bool   = False
Usages = {}


AucMaster:Auctioneer = Auctioneer(auctionchan = "rsay",maxactiveauctions = 3)

# NORMAL COMMANDS
Usages['bid'] = "Usage: !{#id|item link @} #initial [#max=0] [#increment=0] [toon name=sender]"
def exBid(cmd: botCommand) ->str:

    aucId   = int(cmd.regMatch.group("aucId"))      if 'aucId' in cmd.regMatch.groupdict() else -1
    aucItem =     cmd.regMatch.group("aucItem")     if 'aucItem' in cmd.regMatch.groupdict() else ""
    sender  = cmd.Sender
    bidVal  = int(cmd.regMatch.group("bidVal"))
    bidMax  = int(cmd.regMatch.group("bidMax"))     if cmd.regMatch.group("bidMax")     is not None else bidVal
    bidInc  = int(cmd.regMatch.group("bidInc"))     if cmd.regMatch.group("bidInc")     is not None else 1 if cmd.regMatch.group("bidMax")     is not None else 0
    bidder  =     cmd.regMatch.group("proxyToon")   if cmd.regMatch.group("proxyToon")  is not None else sender
    if BotDebug:
        if aucId > 0:
            return "Auctions do not exist but I if they did you would have bid on auction:" + aucId.__str__()
        else:
            return "Auctions do not exist but I if it did you would have bid on item:" + aucItem
    return AucMaster.AddBid(aucId, sender, bidder, aucItem, oDKP.getDKP(bidder), bidVal, bidMax, bidInc)

Usages['admin'] = "Usage: !admin"
def exAdmin(cmd: botCommand) -> str:
    AucMaster.AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

Usages['dkp'] = "Usage: !dkp [toon name=sender]"
def exDKP(cmd: botCommand) -> str:
    name        = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp         = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

Usages['help'] = "Usage: !help [bid|dkp|status]"
def exHelp(cmd: botCommand) -> str:
    validParam = ["bid","dkp","status"]
    catagory = cmd.Params[1] if cmd.ParCount > 0 else ""
    if   catagory == "bid":
        return Usages['bid']
    elif catagory == "dkp":
        return Usages['dkp']
    elif catagory == "status":
        return Usages['status']
    
    return Usages['help']

Usages['status'] = "Usage: !status"
def exStatus(cmd: botCommand) -> str:
    usage = "Status"
    return usage + "Not Implemented"

# ADMIN COMMANDS
Usages['editAuc'] = "Usage: !<#id|'all'> {award|cancel|close|pause|start [#duration] [#quantity] [b:auto award]}"
def exEditAuc(cmd: botCommand) -> str:
    description = "Admin command starting with !<id> are editing existing auctions"
    validChans = ["group","g","raid","rsay","guild","gu"]

    id          = int(cmd.regMatch.group("aucId"))      if cmd.regMatch.group("aucId").lower() != "all" else AucMaster.IDAll
    cmdType     = cmd.regMatch.group("cmdType").lower()
    duration    = float(cmd.regMatch.group("duration")) if cmd.regMatch.group("duration")   is not None else -1.0
    quanity     = int(cmd.regMatch.group("quanity"))    if cmd.regMatch.group("quanity")    is not None else -1
    autoAward   = cmd.regMatch.group("autoAward")       if cmd.regMatch.group("autoAward")  is not None else None
    autoAwardB  = None if (autoAward is None) else (autoAward.lower() == "true") or (autoAward == "1")
    
    if cmdType == "award":
        return AucMaster.AwardAuction(id,autoAwardB)
    if cmdType == "cancel":
        return AucMaster.CancelAuction(id)
    if cmdType == "close":
        return AucMaster.CloseAuction(id)
    if cmdType == "pause":
        return AucMaster.PauseAuction(id)
    if cmdType == "start":
        return AucMaster.StartAuction(id,duration,quanity,autoAwardB)
    
    return "Auctions do not exist yet therefore i cannot " + cmdType + " them"

Usages['auc'] = "Usage: !auc [-{s|a}] item [| item].. @ [#duration=3] [#quantity=1] [autoAward=false]"
def exNewAuc(cmd: botCommand) -> str:
    description = "Admin command starting with !auc are creating new auctions"
    switchOpts  = cmd.regMatch.group("switchOpts") if cmd.regMatch.group("switchOpts") is not None else ""
    itemsStr    = cmd.regMatch.group("items")
    items       = re.split(r'\s*\|\s*',itemsStr)
    duration    = float(cmd.regMatch.group("duration")) if cmd.regMatch.group("duration") is not None else 3
    quanity     = int(cmd.regMatch.group("quanity")) if cmd.regMatch.group("quanity") is not None else 1
    autoStart   = "s" in switchOpts
    autoAward   = "a" in switchOpts
    
    if BotDebug:
        return "Can't start new auction yet on " + itemsStr + " but options would be " + switchOpts + " duration " + duration.__str__() + " quantity " + quanity.__str__()
    return AucMaster.AddAuction(items,duration,quanity,autoStart,autoAward)

Usages['chan'] = "Usage: !chan {group|g|raid|rsay|guild|gu}"
def exChan(cmd: botCommand) -> str:
    description = "Channel Set command configures where auctions will take place."

    validChans = ["group","g","raid","rsay","guild","gu"]

    if not cmd.ParCount > 0: 
        return "Error: no channel specified. " + Usages['chan'] + " Auction channel currently set to: " + AucMaster.AuctionChannel
    if cmd.Params[1] not in validChans:
        return "Error: Channel specified is not in approved list " + Usages['chan'] 
    else:
        AucMaster.AuctionChannel = cmd.Params[1]
        return "Auction channel currently set to: " + AucMaster.AuctionChannel

Usages['clear'] = "Usage: !clear"
def exClear(cmd: botCommand) -> str:
    description = "Clear command deletes all auctions and bids closed active and pending. "
    AucMaster.ClearAuctionsAndBids()
    return "Nuked it ALL, start over. GL"
    
Usages['debug'] = "Usage: !debug"
def exDebug(cmd: botCommand) -> str:
    description = "Debug command toggles the debug state on and off."
    global BotDebug
    BotDebug = not BotDebug
    return "Bot Debug set to " + BotDebug.__str__()

Usages['adminHelp'] = "Usage: !help [auc|chan|editAuc|max|clear|debug|user|admin]"
def exAdminHelp(cmd: botCommand) -> str:
    catagory        = cmd.Params[1] if cmd.ParCount > 0 else ""
    if catagory == "user":
        return exHelp(cmd) + " Must be in a non-Admin channel to use options"    
    if   catagory == "admin":
        return Usages['admin']
    if   catagory == "auc":
        return Usages['auc']
    if   catagory == "chan":
        return Usages['chan']
    if   catagory == "clear":
        return Usages['clear']
    if   catagory == "debug":
        return Usages['debug']
    if   catagory == "editAuc":
        return Usages['editAuc']
    if   catagory == "max":
        return Usages['max']
    
    return Usages['adminHelp']

Usages['max'] = "Usage: !max #num : where <num> is a positive integer."
def exMax(cmd: botCommand) -> str:
    description = "Max command sets the number of concurrent auction"

    if cmd.ParCount > 0 and cmd.Params[1].isnumeric():
        maxAuc = int(cmd.Params[1])
    elif cmd.ParCount > 0:
        return "Error: <num> entered <"+cmd.Params[1]+"> is not a positive integer " + Usages['max']
    else:
        return "Error: No <num> given " + Usages['max'] + "Current max is " + AucMaster.MaxActiveAuctions.__str__()
    if maxAuc < 1:
        return "Error: <num> entered <"+cmd.Params[1]+"> is not positive " + Usages['max']
    AucMaster.MaxActiveAuctions = maxAuc
    return "Max concurrent auctions set to "+ AucMaster.MaxActiveAuctions.__str__()
    

cmdRegistration = {
    "Normal" : {
        "ADMIN"                     : exAdmin,
        "DKP"                       : exDKP,
        "HELP"                      : exHelp,
        "STATUS"                    : exStatus,
        regexHelper.bidWithIDPtrn   : exBid,
        regexHelper.bidWithItemPtrn : exBid
    },
    "Admin" : {
        regexHelper.aucIdCmdsPtrn   : exEditAuc,       
        regexHelper.aucCmdPtrn      : exNewAuc,       
        "CHAN"                      : exChan,
        "CLEAR"                     : exClear,
        "DEBUG"                     : exDebug,
        "HELP"                      : exAdminHelp,
        "MAX"                       : exMax
    }
}

def reply(cmd: botCommand, message: str):
    if(cmd.Channel == "you"): eqApp.tell(cmd.Sender, message)
    else: eqApp.sendMessage(cmd.Channel, message)
    return

def execute(cmd: botCommand):
    if(cmd.Channel == AucMaster.AdminChannel):
        for command in cmdRegistration["Admin"]:
            if regexHelper.eqCommand(command, cmd):
                reply(cmd, cmdRegistration["Admin"][command](cmd))
                return
    for command in cmdRegistration["Normal"]:
        if regexHelper.eqCommand(command, cmd):
            reply(cmd, cmdRegistration["Normal"][command](cmd))
            return
    return

async def runAuctioneer():
    while True:
        AucMaster.Announce()
        await asyncio.sleep(0)
    return
