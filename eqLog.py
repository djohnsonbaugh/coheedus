import appConfig
from os.path import exists
import os
import time
from datetime import datetime
import asyncio

class eqLog(object):
    """description of class"""

    def __init__(self, conf:appConfig):
        self.character = conf.get("EVERQUEST","character","coheedus")
        self.server = conf.get("EVERQUEST","server","thornblade")
        self.eqDir = conf.get("EVERQUEST","eqdir","C:\Everquest")
        return

    def getFileName(self, mod:str = "") ->str:
        return self.eqDir + "\Logs\eqlog_" + self.character + "_" + self.server + mod + ".txt"

    def resetLogFile(self):
        timestamp:str = datetime.now().strftime("%Y%m%d%H%M%S")
        if exists(self.getFileName()):
            os.rename(self.getFileName(),self.getFileName(timestamp))
        with open(self.getFileName(), "w") as f:
            f.write("Log file reset at " + timestamp + ".\n")
        return

    async def monitorLog(self, newLineFunc):
        self.resetLogFile()
        with open(self.getFileName(), 'r') as file:
            line:str = ''
            while True:
                tmp = file.readline()
                if tmp is not None:
                    line += tmp
                    if line.endswith("\n"):
                        newLineFunc(line)
                        line = ''
                    else:
                        await asyncio.sleep(0)
                else: 
                    await asyncio.sleep(0)
        return