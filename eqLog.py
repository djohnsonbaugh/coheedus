import appConfig
from os.path import exists
import os
import winOS
import time
from datetime import datetime
from multiprocessing import Queue
import regexHelper
from botCommand import botCommand

class eqLog(object):
    """description of class"""

    def __init__(self, conf:appConfig, cmdque, guildmessageque,eqmessage):
        self.character = conf.get("EVERQUEST","character","coheedus")
        self.server = conf.get("EVERQUEST","server","thornblade")
        self.eqDir = conf.get("EVERQUEST","eqdir","C:\Everquest")
        self.CMDQue = cmdque
        self.GuildMessageQue = guildmessageque
        self.EQMessageVerificationQue = eqmessage
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
        elif regexHelper.isEQBotMessage(line,cmd):
            #print("something happend: " + str(cmd)) 
            self.EQMessageVerificationQue.put(cmd)
        elif regexHelper.isGuildMessage(line, cmd):
            self.GuildMessageQue.put(cmd)
        elif regexHelper.isGuildAchievement(line,cmd):
            self.GuildMessageQue.put(cmd)
            if "Keeper" in line or "Reign" in cmd.Text:
                aacmd = botCommand()
                parts = cmd.Text.split(' ')
                aacmd.set(parts[0],"you","aa " + cmd.Text)
                self.CMDQue.put(aacmd)
        elif regexHelper.isEQRaidRosterChange(line, cmd):
            self.CMDQue.put(cmd)
        elif regexHelper.isEQRaidRosterDump(line, cmd):
            self.CMDQue.put(cmd)

        #else:
        #    print(line, end='')
        return

    def monitorLog(self):
        self.resetLogFile()
        with open(self.getFileName(), 'r') as file:
            line:str = ''
            while winOS.isParentAlive():
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
        print("Log parent dead - goodbye")
        return