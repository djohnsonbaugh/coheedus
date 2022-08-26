#import eqApp
from appConfig import appConfig
from openDKP import openDKP
from botCommand import botCommand
import regexHelper
from auctioneer import Auctioneer
import asyncio
import re
from multiprocessing import Queue
from datetime import datetime, timedelta
import time
import winOS
import gsheets
from winOS import winKey
oDKP : openDKP = None

DiscordReplyCallBack = None
CommandQue:Queue =None
EQMessageQue:Queue=None
AucMaster:Auctioneer = None
PlayerName:str = ""

def init(config: appConfig, cmdque:Queue, eqmessage:Queue):
    global oDKP, CommandQue, EQMessageQue, AucMaster, PlayerName
    oDKP = openDKP(config)
    DiscordReplyCallBack = None #discordreply
    CommandQue = cmdque
    EQMessageQue = eqmessage
    gsheets.init()
    AucMaster = Auctioneer(auctionchan = "rsay",maxactiveauctions = 3, eqmessage= EQMessageQue)
    PlayerName = config.get("EVERQUEST", "character", "Coheedus")
    return

BotDebug:bool   = False
Usages = {}
AdminUsages = {}

# RAID STRAT
RaidStrats = {}




# NORMAL COMMANDS
Usages['bid'] = \
"Usage: !{#id|s:item_link @} #initial [#max=0] [#increment=0] [w:toon_name=sender]\n"+\
"Bidding: To bid send a tell to me begining with ! followed by either the auction ID number or item link. Item links must be followed by @\n"+\
"The bid is comprised of 1 to 3 numbers separated by a space.\n"+\
"The first number is starting bid. Second (optional) is your max bid. Third (optional) is how much to increment your bid by until you are either winning or at max default increment is 1\n"+\
"To bid for one of YOUR boxes from a different character type the toon name at the end of the line.\n"+\
"For examples type !help bid_id or !help bid_name"

Usages['bid_id'] = \
"Usage: !#id #initial [#max=0] [#increment=0] [w:toon_name=sender]\n"+\
"Bid 7 on auciton 3 <Example> !3 7\n"+\
"Bid 7 now & auto raise until 97 on auction 3 <Example> !3 7 97\n"+\
"Bid 7 now & auto raise until 97 increment bids by 5 on auction 3 <Example> !3 7 97 5\n"+\
"Bid 7 now & auto raise until 97 on auction 3 for your box Mitsuki <Example> !3 7 97 Mitsuki"

Usages['bid_name'] = \
"Usage: !s:item_link @ #initial [#max=0] [#increment=0] [w:toon_name=sender]\n"+\
"Bid 5 on bone chip <Example> !bone chip@5\n"+\
"Bid for your box Mitsuki <Example> !bone chip@ 5 Mitsuki\n"+\
"Bid for your box Mitsuki with max bid 70 <Example> !bone chip @1 70 Mitsuki\n"+\
"Bid for your box Mitsuki with max bid 70 and increment by 5 <Example> !bone chip@ 1 70 5 Mitsuki"

def exBid(cmd: botCommand) ->str:

    aucId   = int(cmd.regMatch.group("aucId"))      if 'aucId' in cmd.regMatch.groupdict() else -1
    aucItem =     cmd.regMatch.group("aucItem")     if 'aucItem' in cmd.regMatch.groupdict() else ""
    sender  = cmd.Sender
    bidVal  = int(cmd.regMatch.group("bidVal"))
    bidMax  = int(cmd.regMatch.group("bidMax"))     if cmd.regMatch.group("bidMax")     is not None else bidVal
    bidInc  = int(cmd.regMatch.group("bidInc"))     if cmd.regMatch.group("bidInc")     is not None else 1
    bidder  =     cmd.regMatch.group("proxyToon")   if cmd.regMatch.group("proxyToon")  is not None else sender
    if BotDebug:
        if aucId > 0:
            return "Auctions do not exist but I if they did you would have bid on auction:" + aucId.__str__()
        else:
            return "Auctions do not exist but I if it did you would have bid on item:" + aucItem
    return AucMaster.AddBid(aucId, sender, bidder, aucItem, oDKP.getDKP(bidder), bidVal, bidMax, bidInc)

def exAA(cmd: botCommand)->str:
    name = cmd.Sender
    aa = cmd.Text
    success = False
    if "Gift" in aa:
        success = gsheets.setFlagStatusAll(name, "T1", 4)
    elif "Tenacity" in aa or "Valor" in aa:
        success = gsheets.setFlagStatusAll(name, "T2", 5)
    elif "Embrace" in aa:
        success = gsheets.setFlagStatusAll(name, "T3", 6)
    elif "Power" in aa:
        success = gsheets.setFlagStatusAll(name, "T4", 3)
    elif "Fervor" in aa or "Sanctity" in aa:
        success = gsheets.setFlagStatusAll(name, "T5", 3)
        
    return "Flags for " + name + " have been updated in the guild spreadsheet. Congratz!" if success else ""

AdminUsages['admin'] = \
"Usage: !admin\n"+\
"Admin command: Type this command in the channel you want to enable to send admin commands and receive admin messages"+\
"But if you are able to see this message then you are already in the admin channel. So this is a pointless message"
def exAdmin(cmd: botCommand) -> str:
    AucMaster.AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

Usages['don'] = \
"Usage: !DoN flagname [value=True] [toon name=sender]"+\
"DoN flag update: Use this command to update the DoN progression spreadsheet by providing the flag name i.e. 'T1', 'T2G2' 'T3R1' from the 4th row"
def exDoN(cmd: botCommand) -> str:
    name        = cmd.Sender
    if(cmd.ParCount <1):
        return "Please provide the flag name from the 4th row of the spreadsheet i.e. !don flagname"
    flag = cmd.Params[1].strip()
    value = None
    if(cmd.ParCount > 1):
        if (cmd.Params[2] == "0" or cmd.Params[2].upper() == "FALSE"):
            value = False
        elif cmd.Params[2] == "1" or cmd.Params[2].upper() == "TRUE":
            value = True
        else:
            name = cmd.Params[2]
    if (cmd.ParCount > 2):
        name = cmd.Params[3]

    if(value is None):
        status:bool = gsheets.getFlagStatus(name, flag)
        if(status is None):
            return "The flag " + flag + " or the character " + name + " was not found in the records."
        else:
            if(status):
                return name + " does have " + flag + " complete."
            else:
                return name + " does NOT have " + flag + " complete."
    else:
        status = gsheets.setFlagStatus(name, flag, value)
        if(status):
            return name +"'s " + flag + " has been updated successfully."
        else:
            return "The flag " + flag + " or the character " + name + " was not found in the records."

    return "something went horribly wrong."

Usages['dkp'] = \
"Usage: !dkp [toon name=sender]"+\
"DKP request: Use this command to request the current dkp balance for yourself (default) or any toon by entering the name"
def exDKP(cmd: botCommand) -> str:
    name        = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp         = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

Usages['help'] = \
"Usage: !help [bid|dkp|status]\n"+\
"Help: Use this command to get usage description and examples of how to interact with me\n"+\
"To receive information about how to bid type: !help bid\n"+\
"How to interpret usage statments.\n"+\
" | means separate the options available for that parameter so for help your options are bid or dkp or status\n"+\
" # means that parameter must be a number only\n"+\
"b: means that parameter is a boolean [0|1|True|False]\n"+\
"w: means that parameter is a single word\n"+\
"s: means that parameter is a string matching everything except the symbol after listed after the parameter\n"+\
"{} means one of the options inside the brakets are required\n"+\
"[] means this parameter is optional. If there are multiple optional parameters in a row of the same type to use one all preceeding must be present"
def exHelp(cmd: botCommand) -> str:
    
    catagory = cmd.Params[1] if cmd.ParCount > 0 else None
    if catagory in Usages:
        return Usages[catagory]
    return Usages['help']
    
Usages['status'] = \
"Usage: !status\n"+\
"Not Implemented"
def exStatus(cmd: botCommand) -> str:
    return Usages['status']

# ADMIN COMMANDS
AdminUsages['editAuc'] = \
"Usage: !<#id|all> {award|cancel|close|pause|start [#duration] [#quantity] [b:auto award]}\n"+\
"Edit Auction admin command"
def exEditAuc(cmd: botCommand) -> str:
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

AdminUsages['auc'] = \
"Usage: !auc [-{s|a}] s:item [| s:item].. @ [#duration=3.0] [#quantity=1] [b:autoAward=false]\n"+\
"Create Auction Admin command.\n"+\
"-s will start auction immediately after creation if max number of auctions running then it will wait in queue\n"+\
"-a will set the auction to auto award the winner when time runs out.\n"+\
"For multiple - options do no use more than one -. Example: -sa\n"+\
"For multiple items separate item links by | and list all before the @ symbol\n"+\
"Duration will accept decimals, but must start with a digit. To have time less than 1 preceed the decimal with a 0"
def exNewAuc(cmd: botCommand) -> str:
    switchOpts  = cmd.regMatch.group("switchOpts") if cmd.regMatch.group("switchOpts") is not None else ""
    itemsStr    = cmd.regMatch.group("items")
    items       = re.split(r'\s*\|\s*',itemsStr)
    duration    = float(cmd.regMatch.group("duration")) if cmd.regMatch.group("duration") is not None else 3
    quanity     = int(cmd.regMatch.group("quanity")) if cmd.regMatch.group("quanity") is not None else 1
    autoStart   = "s" in switchOpts
    autoAward   = "a" in switchOpts
    result = AucMaster.AddAuction(items,duration,quanity,autoStart,autoAward)
    if BotDebug:
        return "Can't start new auction yet on " + itemsStr + " but options would be " + switchOpts + " duration " + duration.__str__() + " quantity " + quanity.__str__()+"\n" + result
    return result

AdminUsages['chan'] = \
"Usage: !chan {group|g|raid|rsay|guild|gu}\n"+\
"Channel set command changes what channel auctions annoucements go"
def exChan(cmd: botCommand) -> str:
    description = "Channel Set command configures where auctions will take place."

    validChans = ["group","g","raid","rsay","guild","gu"]

    if not cmd.ParCount > 0: 
        return "Error: no channel specified. Auction channel currently set to: " + AucMaster.AuctionChannel +"\n" + AdminUsages['chan']
    if cmd.Params[1] not in validChans:
        return "Error: Channel specified is not in approved list " + AdminUsages['chan'] 
    else:
        AucMaster.AuctionChannel = cmd.Params[1]
        return "Auction channel currently set to: " + AucMaster.AuctionChannel

AdminUsages['clear'] = \
"Usage: !clear\n"+\
"Clear command deletes all auctions and bids closed active and pending."
def exClear(cmd: botCommand) -> str:
    description = "Clear command deletes all auctions and bids closed active and pending. "
    AucMaster.ClearAuctionsAndBids()
    return "Nuked it ALL, start over. GL"
    
AdminUsages['debug'] = \
"Usage: !debug\n"+\
"Debug command toggles the debug state on and off."
def exDebug(cmd: botCommand) -> str:
    global BotDebug
    BotDebug = not BotDebug
    return "Bot Debug set to " + BotDebug.__str__()
    
AdminUsages['max'] = \
"Usage: !max #num\n"+\
"Max command sets the number of concurrent auction"
def exMax(cmd: botCommand) -> str:

    if cmd.ParCount > 0 and cmd.Params[1].isnumeric():
        maxAuc = int(cmd.Params[1])
    elif cmd.ParCount > 0:
        return "Error: <num> entered <"+cmd.Params[1]+"> is not a positive integer " + AdminUsages['max']
    else:
        return "Error: No <num> given " + AdminUsages['max'] + "Current max is " + AucMaster.MaxActiveAuctions.__str__()
    if maxAuc < 1:
        return "Error: <num> entered <"+cmd.Params[1]+"> is not positive " + AdminUsages['max']
    AucMaster.MaxActiveAuctions = maxAuc
    return "Max concurrent auctions set to "+ AucMaster.MaxActiveAuctions.__str__()

helpOpts = ""
for i, k in enumerate(sorted(Usages.keys())):
    helpOpts += k.__str__() if i == len(Usages)-1 else k.__str__() + "|"

Usages['help'] = \
"Usage: !help ["+helpOpts+"]\n"+\
"Help: Use this command to get usage description and examples of how to interact with me\n"+\
"To receive information about how to bid type: !help bid\n"+\
"How to interpret usage statments.\n"+\
" | means separate the options available for that parameter so for help your options are bid or dkp or status\n"+\
" # means that parameter must be a number only\n"+\
"b: means that parameter is a boolean [0|1|True|False]\n"+\
"w: means that parameter is a single word\n"+\
"s: means that parameter is a string matching everything except the symbol after listed after the parameter\n"+\
"{} means one of the options inside the brakets are required\n"+\
"[] means this parameter is optional. If there are multiple optional parameters in a row of the same type to use one all preceeding must be present\n"

def exHelp(cmd: botCommand) -> str:
    
    catagory = cmd.Params[1] if cmd.ParCount > 0 else None
    if catagory in Usages:
        return Usages[catagory]
    return Usages['help']

raidOpts = ""
for i, k in enumerate(sorted(RaidStrats.keys())):
    raidOpts += k.__str__() if i == len(RaidStrats)-1 else k.__str__() + "|"

RaidStrats['raid'] = \
"Usage: !raid ["+raidOpts+"]\n"+\
"Raid : Use this command print raid fight strat summaries and cheat sheets\n"
def exRaid(cmd: botCommand) -> str:
    
    catagory = cmd.Params[1] if cmd.ParCount > 0 else None
    if catagory in RaidStrats:
        return RaidStrats[catagory]
    return RaidStrats['raid']

#RaidStrats['raid'] = \
#"Usage: !raid ["+raidOpts+"]\n"+\
#"Raid : Use this command print raid fight strat summaries and cheat sheets\n"
def exRod(cmd: botCommand) -> str:
    if PlayerName.lower() == "coheedus":
        winOS.pushKey(winKey.kM)
        return ""
    return "?"

adminHelpOpts = ""
for i, k in enumerate(sorted(AdminUsages.keys())):
    adminHelpOpts += k.__str__() if i == len(AdminUsages)-1 else k.__str__() + "|"
    
AdminUsages['adminHelp'] = \
"Usage: !help ["+adminHelpOpts+"]\n"+\
"Help in this admin channel allows you to query usages descriptions and examples of admin commands\n"+\
"To see general user help with explanation of usage statements type '!help user'"

def exAdminHelp(cmd: botCommand) -> str:
    catagory = cmd.Params[1] if cmd.ParCount > 0 else None
    if catagory == "user":
        return "Must be in a non-Admin channel to query none admin commands:\n" + exHelp(cmd)    
    if catagory in AdminUsages:
        return AdminUsages[catagory]
    return AdminUsages['adminHelp']

#Discord Commands
def exPrintToGuild(cmd: botCommand)->str:
    cmd.Channel = "guild"
    return "<" + cmd.Sender + "> " + cmd.Text

cmdRegistration = {
    "Normal" : {
        "ADMIN"                     : exAdmin,
        "DKP"                       : exDKP,
        "DON"                       : exDoN,
        "AA"                        : exAA,
        "HELP"                      : exHelp,
        "RAID"                      : exRaid,
        "ROD"                       : exRod,
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
    },
    "Discord" : {
        "DEFAULT"                   : exPrintToGuild
    }
}

def reply(cmd: botCommand, message: str):
    if message == "":
        return
    messages = message.split("\n")
    for line in messages:   
        if(cmd.Channel == "you"): EQMessageQue.put(("tell " + cmd.Sender, line))
        elif(cmd.Channel == "discord"): DiscordReplyCallBack(line)
        else: EQMessageQue.put((cmd.Channel, line))
        #else: eqApp.sendMessage(cmd.Channel, line)
    return

def execute(cmd: botCommand):
    if(cmd.Channel == "discord"):
        for command in cmdRegistration["Discord"]:
            if regexHelper.eqCommand(command, cmd):
                reply(cmd, cmdRegistration["Discord"][command](cmd))
                return
        reply(cmd, cmdRegistration["Discord"]["DEFAULT"](cmd))
    else:
        if(cmd.Channel == AucMaster.AdminChannel):
            for command in cmdRegistration["Admin"]:
                if regexHelper.eqCommand(command, cmd):
                    reply(cmd, cmdRegistration["Admin"][command](cmd))
                    return
        for command in cmdRegistration["Normal"]:
            if regexHelper.eqCommand(command, cmd):
                reply(cmd, cmdRegistration["Normal"][command](cmd))
                return
        reply(cmd, "?")
    return

def runAuctioneer():
    last:datetime = datetime.now()
    while winOS.isParentAlive():
        if not CommandQue.empty():
            try:
                cmd = CommandQue.get_nowait()
            except:
                print("Command Que Get Error: " + str(cmd))
            execute(cmd)
        messagecount = AucMaster.Announce()
        if messagecount == 0 and datetime.now() - last > timedelta(minutes=5):
            time.sleep(3)
        else:
            last = datetime.now()
    print("Auc parent dead - goodbye")
    return