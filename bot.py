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
        self.Text = text
        return