import appConfig
from os.path import exists
import os
import time
from datetime import datetime
from multiprocessing import Queue
import regexHelper
from botCommand import botCommand

class eqLog(object):
    """description of class"""

    def __init__(self, conf:appConfig, cmdque, guildmessageque):
        self.character = conf.get("EVERQUEST","character","coheedus")
        self.server = conf.get("EVERQUEST","server","thornblade")
        self.eqDir = conf.get("EVERQUEST","eqdir","C:\Everquest")
        self.CMDQue = cmdque
        self.GuildMessageQue = guildmessageque
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

    def eventNewLogLine(self,line:str):
        cmd : botCommand = botCommand()
        if regexHelper.isCommand(line, cmd):
            print(line, end='')
            self.CMDQue.put(cmd)
        elif regexHelper.isGuildMessage(line, cmd):
            print(line, end='')
            self.GuildMessageQue.put(cmd)
            print("I put" + str(cmd) + " in the que and the lenght is " + str(self.GuildMessageQue.qsize()))
        #else:
        #    print(line, end='')
        return

    def monitorLog(self):
        self.resetLogFile()
        with open(self.getFileName(), 'r') as file:
            line:str = ''
            while True:
                tmp = file.readline()
                if tmp is not None:
                    line += tmp
                    if line.endswith("\n"):
                        self.eventNewLogLine(line)
                        line = ''
                    elif line == '':
                        time.sleep(1)
                else: 
                    time.sleep(1)
        return