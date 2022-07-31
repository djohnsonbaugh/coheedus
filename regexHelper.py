import re
from botCommand import botCommand
commandPattern = re.compile("(?x)\[[A-Za-z0-9: ]+\]\s([a-zA-Z]+)\stells\s(the\s)?([a-zA-Z]+:)?(group|guild|raid|you|\d+),\s'\w*!(.*)'")
intPattern = re.compile("\d+")

def isCommand(line:str, cmd: botCommand) -> bool:
    if(commandPattern.match(line)):
        result = commandPattern.search(line)
        cmd.set(result.group(1).strip(), result.group(4).strip(), result.group(5).strip())
        return True
    return False

def equalsCommand(cmdpattern:str, cmd:str)->bool:
    if(re.match("(?xi)" + cmdpattern,cmd)): return True
    return False

def equalsCommand(cmdpattern:re.Pattern, cmd:str)->bool:
    if(re.match(cmdpattern,cmd)): return True
    return False