from configparser import RawConfigParser
from os.path import exists

class appConfig(object):
    """description of class"""


    def __init__(self):
        self.filename = "config.ini"
        self.config = RawConfigParser()
        self.readConfig()

    def readConfig(self):
        if(exists(self.filename)):
            self.config.read(self.filename)
        return

    def writeConfig(self):
        with open(self.filename, 'w') as conf:
            self.config.write(conf)
        return

    def get(self, section: str, option: str, default:str) -> str:
        if not self.config.has_option(section,option):
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config[section][option] = default
            self.writeConfig()
        return self.config[section][option]

    def set(self, section: str, option: str, value:str):
        if not self.config.has_option(section,option):
            if not self.config.has_section(section):
                self.config.add_section(section)
        self.config[section][option] = value
        self.writeConfig()
        return


    def getBool(self, section: str, option: str, default:bool) -> bool:
        return (self.get(section, option, default.__str__()) == 'True')
