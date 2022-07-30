import re
from bot import botCommand
commandPattern = re.compile("(?x)\[[A-Za-z0-9: ]+\]\s([a-zA-Z]+)\stells\s(the\s)?([a-zA-Z]+:)?(guild|raid|you|\d+),\s'!(.*)'")

def isCommand(line:str, cmd: botCommand) -> bool:
    if(commandPattern.match(line)):
        result = commandPattern.search(line)
        cmd.set(result.group(1).strip(), result.group(4).strip(), result.group(5).strip())
        return True
    return False
