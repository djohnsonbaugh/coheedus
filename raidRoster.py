from datetime import datetime, timedelta

class raidRoster(object):
    """description of class"""

    def __init__(self,name:str, start:datetime=datetime.today+timedelta(hours=19,minutes=30), tickperiod: int =15, dkpvalue:float = 0.5):
        self.__name = name
        self.__roster:{str,[(datetime,datetime)]} = {}
        self.__lastRaidDump = datetime.min()
        self.__startTime = start
        self.__tickPeriod = tickperiod
        self.__dkpValue = dkpvalue

    def addAttendanceRecord(name:str, leaving:bool = False):
        if name not in self.__roster.keys():
            self.__roster[name] = []
        for start,end in self.__roster[name]:
            if end == datetime.max():
               if leaving:
                    end = datetime.now()
               return
        if(leaving):
            self.__roster[name].append((self.__lastRaidDump, datetime.now()))
        else:
            self.__roster[name].append((datetime.now(), datetime.max()))
        return

    def __attended(name:str, ticktime:datetime, duration:timedelta)->bool:
        attdur:timedelta = timedelta(0)
        for start,end in self.__roster[name]:
            if start < ticktime and end > ticktime - duration:
                attdur += min(start,ticktime-duration) - max(end, ticktime)
        return attdur > duration/2

    def getAttendance(ticktime:datetime, duration:timedelta)->[str]:
        toons:[str] = []
        for name in self.__roster.keys():
            if self.__attended(name, ticktime, duration):
                toons.append(name)
        return toons

    def addRaidDump(names:[str]):
        for name in self.__roster.keys():
            self.addAttendanceRecord(name, name in names)
        for name in names:
            if name not in self.roster.keys():
                self.addAttendanceRecord(name)
        self.__lastRaidDump = datetime.now()
        return

    def AddKill(name:str, duration:int = 20, value:int = 1):
        toons:[str] = self.getAttendance(datetime.now(), timedelta(mintues=duration))

        return