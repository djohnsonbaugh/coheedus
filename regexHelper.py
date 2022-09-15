import re
from botCommand import botCommand
commandPattern = re.compile("\[[\w\d: ]+\]\s(\w+)\stells\s(the\s)?(\w+:)?(group|guild|raid|you|\d+),\s'\s*!(.*)'")
aucCmdPtrn = re.compile("^\s*auc\s+((?P<switchOpts>-[sa]+)\s*)?((?P<items>[^\n\r@]+[^\s@])\s*)(@\s*(?P<duration>\d+\.?\d*)(\s+(?P<quanity>\d+))?)?")
aucIdCmdsPtrn = re.compile("(?i)^\s*(?P<aucId>all|\d+)\s+(?P<cmdType>award|pause|close|start|cancel)\s*(?P<duration>\d+\.?\d*)?(\s+(?P<quanity>\d+)?)?(\s+(?P<autoAward>0|1|true|false)?)?")
bidWithIDPtrn = re.compile("^\s*(bid\s+)?(?P<aucId>\d+)\s*(\s|@)\s*?(?P<bidVal>\d+)(\s+(?P<bidMax>\d+))?(\s+(?P<bidInc>-?[\d]+))?(\s*(?P<proxyToon>\w+))?")
bidWithItemPtrn = re.compile("^\s*(bid\s+)?(?P<aucItem>[^\n\r@<>[\]{}$~_]*[a-zA-Z][^\n\r@<>[\]{}$~_]*?)\s*@\s*(?P<bidVal>\d+)(\s+(?P<bidMax>\d+))?(\s+(?P<bidInc>-?[\d]+))?(\s*(?P<proxyToon>\w+))?")
guildMessagePattern = re.compile("\[[\w\d: ]+\]\s(\w+)\stells\sthe\sguild,\s'(.*)'")
achievementPattern = re.compile("\[[\w\d: ]+\]\s+Your\sguildmate\s+(\w*\s+has\scompleted.*(Alternate\sAdvancement|Reign|Keeper|Hunter|Epic|Level).*achievement\.)")
botMessagePattern = re.compile("\[[\w\d: ]+\]\s(You\s((tell|say\sto)\s(your\s)?(\w+:)?(party|guild|raid|\d+)|told\s(\w+)),\s'(.*)'|(\w+)\sis\snot\sonline\sat\sthis\stime.)")
raidRosterChange = re.compile("\[[\w\d: ]+\]\s(\w+)\s(?:were\s|have\s|has\s)?(removed|joined|formed|left)\s(?:from\s)?(?:the\s|a\s)?raid.")
raidRosterDump = re.compile("\[[\w\d: ]+\]\sOutputfile\sComplete:\s(RaidRoster_\w+-\d+-\d+.txt)")

def isCommand(line:str, cmd: botCommand) -> bool:
    if(commandPattern.match(line)):
        result = commandPattern.search(line)
        cmd.set(result.group(1).strip(), result.group(4).strip(), result.group(5).strip())
        return True
    return False

def isGuildAchievement(line:str, cmd: botCommand)->bool:
    if(achievementPattern.match(line)):
        result = achievementPattern.search(line)
        cmd.set("Everquest", "Achievement", result.group(1).strip())
        return True
    return False

def isGuildMessage(line:str, cmd: botCommand)->bool:
    if(guildMessagePattern.match(line)):
        result = guildMessagePattern.search(line)
        cmd.set(result.group(1).strip(), "", result.group(2).strip())
        return True
    return False

def isEQBotMessage(line:str, cmd: botCommand)->bool:
    if(botMessagePattern.match(line)):
        result = botMessagePattern.search(line)
        if result.group(9) is None:
            cmd.set(result.group(7).strip() if result.group(7) is not None else "", result.group(6).strip() if result.group(6) is not None else "", result.group(8).strip() if result.group(8) is not None else "")
        else:
            cmd.set(result.group(9).strip(),"",None)
        return True
    return False


def equalsCommandStr(cmdpattern:str, cmd: botCommand)->bool:
    if(re.match("(?xi)" + cmdpattern,cmd.Cmd)): return True
    return False

def equalsCommand(cmdpattern:re.Pattern, cmd: botCommand)->bool:
    if(re.match(cmdpattern,cmd.Text)):
        cmd.regMatch = cmdpattern.search(cmd.Text)
        return True
    return False

def eqCommand(cmdpattern, cmd:botCommand) ->bool:
    if(type(cmdpattern) == str): return equalsCommandStr(cmdpattern,cmd)
    return equalsCommand(cmdpattern,cmd)

def isEQRaidRosterChange(line:str, cmd: botCommand)->bool:
    if(raidRosterChange.match(line)):
        result = raidRosterChange.search(line)
        cmd.set(result.group(1).strip(),"log","updateraidroster " + result.group(2).strip())
        return True
    return False

def isEQRaidRosterDump(line:str, cmd: botCommand)->bool:
    if(raidRosterDump.match(line)):
        result = raidRosterDump.search(line)
        cmd.set("Everquest","log","readraidrosterdump " + result.group(1).strip())
        return True
    return False
