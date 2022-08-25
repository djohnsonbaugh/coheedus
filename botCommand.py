import re
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
        self.regMatch:re.Match = None
        params: [str] = text.split(' ') if text is not None else []

        for param in params:
            self.Params.append(param.strip())
        self.Cmd:str = self.Params[0].upper() if len(self.Params) > 0 else ""
        self.ParCount: int = len(self.Params)- 1
        return

    def __str__(self):
        return self.Sender + "(" +self.Channel + ") " + (self.Text if self.Text is not None else "")

    def __repr__(self):
        return self.Sender + "(" +self.Channel + ") " + (self.Text if self.Text is not None else "")