import re
from botCommand import botCommand
commandPattern = re.compile("(?x)\[[A-Za-z0-9: ]+\]\s([a-zA-Z]+)\stells\s(the\s)?([a-zA-Z]+:)?(group|guild|raid|you|\d+),\s'\w*!(.*)'")
aucIDPattern = re.compile("(\d+)(\w+.*)?")

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