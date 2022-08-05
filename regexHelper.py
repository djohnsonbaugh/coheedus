import re
from botCommand import botCommand
commandPattern = re.compile("\[[\w\d: ]+\]\s(\w+)\stells\s(the\s)?(\w+:)?(group|guild|raid|you|\d+),\s'\w*!(.*)'")
aucCmdPtrn = re.compile("^\s*auc\s+((?P<switchOpts>-[sa]+)\s*)?((?P<items>[^\n\r@]+[^\s@])\s*)(@\s*(?P<duration>\d+\.?\d*)(\s+(?P<quanity>\d+))?)?")
aucIdCmdsPtrn = re.compile("(?i)^\s*(?P<aucId>all|\d+)\s+(?P<cmdType>award|pause|close|start|cancel)\s*(?P<duration>\d+\.?\d*)?(\s+(?P<quanity>\d+)?)?(\s+(?P<autoAward>0|1|true|false)?)?")
bidWithIDPtrn = re.compile("^\s*(?P<aucId>\d+)\s*(\s|@)\s*?(?P<bidVal>\d+)(\s+(?P<bidMax>\d+))?(\s+(?P<bidInc>-?[\d]+))?(\s*(?P<proxyToon>\w+))?")
bidWithItemPtrn = re.compile("^\s*(?P<aucItem>[^\n\r@<>[\]{}$~_]*[a-zA-Z][^\n\r@<>[\]{}$~_]*?)\s*@\s*(?P<bidVal>\d+)(\s+(?P<bidMax>\d+))?(\s+(?P<bidInc>-?[\d]+))?(\s*(?P<proxyToon>\w+))?")

def isCommand(line:str, cmd: botCommand) -> bool:
    if(commandPattern.match(line)):
        result = commandPattern.search(line)
        cmd.set(result.group(1).strip(), result.group(4).strip(), result.group(5).strip())
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