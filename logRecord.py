from enum import Enum

class logType(Enum):
    Bid=1
    Auction=2
    Admin=3

class logRecord(object):
    """description of class"""


    def __init__(self, type:logType, text:str, sender:str ='bot'):
        self.Sender = sender
        self.Type:logType = type
        self.Text = text
        return