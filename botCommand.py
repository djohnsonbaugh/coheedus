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