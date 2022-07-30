import eqApp
from appConfig import appConfig
from openDKP import openDKP
oDKP : openDKP = None
def initConfig(config: appConfig):
    global oDKP
    oDKP = openDKP(config)
    return

class botCommand(object):
    """description of class"""

    def __init__(self):
        self.Sender = ""
        self.Channel = ""
        self.Text = ""
        return

    def set(self, sender: str, channel: str, text:str):
        self.Sender = sender
        self.Channel = channel
        if(self.Channel == "group"): self.Channel = "g"
        if(self.Channel == "raid"): self.Channel = "rsay"
        self.Text = text
        self.Params: [str] = []
        params: [str] = text.split(' ')
        for param in params:
            self.Params.append(param.strip())
        self.Cmd:str = self.Params[0].upper()
        self.ParCount: int = len(self.Params)- 1
        return

AdminChannel = ""
AuctionChannel = "rsay"

def reply(cmd: botCommand, message: str):
    if(cmd.Channel == "you"): eqApp.tell(cmd.Sender, message)
    else: eqApp.sendMessage(cmd.Channel, message)
    return

def exDKP(cmd: botCommand) -> str:
    name = cmd.Params[1] if cmd.ParCount > 0 else cmd.Sender
    dkp = oDKP.getDKP(name)
    return dkp.__str__() + " DKP for " + name

def exAdmin(cmd: botCommand) -> str:
    global AdminChannel
    AdminChannel = cmd.Channel
    return "Admin Commands & Messages Here"

def exChan(cmd: botCommand) -> str:
    global AuctionChannel
    if(cmd.ParCount > 0):
        AuctionChannel = cmd.Params[1]
    return "Auction channel currently set to: " + AuctionChannel


cmdRegistration = {
    "Normal" : {
        "DKP"   : exDKP,
        "ADMIN" : exAdmin
    },
    "Admin" : {
        "CHAN"   : exChan,       
    }
}

def execute(cmd: botCommand):
    for command in cmdRegistration["Normal"]:
        if command == cmd.Cmd:
            reply(cmd, cmdRegistration["Normal"][command](cmd))
            return
    if(cmd.Channel == AdminChannel):
        for command in cmdRegistration["Admin"]:
            if command == cmd.Cmd:
                reply(cmd, cmdRegistration["Admin"][command](cmd))
                return
    return

