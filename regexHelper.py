import re
from botCommand import botCommand
commandPattern = re.compile("\[[\w\d: ]+\]\s(\w+)\stells\s(the\s)?(\w+:)?(group|guild|raid|you|\d+),\s'\w*!(.*)'")
dkpCmdPtrn = re.compile("^\s*dkp\s+(?<toon>\w+)")
aucCmdPtrn = re.compile("^\s*auc\s+((<switchOpts>-[sa]+)\s*)?((?<items>[^\n\r@]+[^\s@])\s*)(@\s*(?<duration>\d+)(\s+(?<quanity>\d+))?)?")
aucIdCmdsPtrn = re.compile("^\s*(?<bidId>\d+)\s+(?<cmdType>pause|close|start|award)\s*(?<length>\d+)?")
bidWithIDPtrn = re.compile("^\s*(?<bidId>\d+)\s+(?<bidVal>\d+)(\s+(?<bidMax>\d+))?(\s+(?<bidInc>-?[\d]+))?(\s*(?<proxyToon>\w+))?")
bidWithItemPtrn = re.compile("^\s*(?<bidItem>[^\n\r@]+?)\s*@\s*(?<bidVal>\d+)(\s+(?<bidMax>\d+))?(\s+(?<bidInc>-?[\d]+))?(\s*(?<proxyToon>\w+))?")

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