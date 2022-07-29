########################################
#All Everquest Application Interaction
########################################
import winOS
import time
import pyperclip
from winOS import winKey
import appConfig

#Global Initialization
EQWindowName:str = "EverQuest"
PasteKey:winKey = winKey.kV
PasteKeyShift:bool = False
PasteKeyCtrl:bool = True
PasteKeyAlt:bool = False

def initConfig(config: appConfig):
    global EQWindowName
    global PasteKey, PasteKeyCtrl, PasteKeyShift, PasteKeyAlt
    EQWindowName = config.get("EVERQUEST", "appName", EQWindowName)
    pkey:str = config.get("EVERQUEST","pasteKey", PasteKey.name)
    PasteKey = winKey[pkey]
    PasteKeyCtrl = config.getBool("EVERQUEST","pasteKeyCtrl", PasteKeyCtrl)
    PasteKeyShift = config.getBool("EVERQUEST","pasteKeyShift", PasteKeyShift)
    PasteKeyAlt = config.getBool("EVERQUEST","pasteKeyAlt", PasteKeyAlt)
    return
     

def isEQActive() ->bool:
    return (winOS.getActiveWindow() == EQWindowName)

def activateEQ() ->bool:
    return winOS.actviateFirstWindow(EQWindowName)

#Copies command to clipboard and pastes it into EQ (assumes EQ is the active window -> use enterCommandSafe)
def enterCommand(command:str) -> bool:
    pyperclip.copy(command)
    winOS.pushKey(winKey.Enter)
    time.sleep(.1)
    winOS.pushKey(PasteKey, PasteKeyShift, PasteKeyCtrl, PasteKeyAlt)
    time.sleep(.1)
    winOS.pushKey(winKey.Enter)
    return True

#Ensurses EQ is active before executing command and will activate EQ when 'force' is True if necessary then return to previous window
def enterCommandSafe(command:str, force:bool=False)->bool:
    if(isEQActive()):
        return enterCommand(command)
    else:
        if(force):
            return winOS.toggleWindowForFunction(EQWindowName, enterCommand, command)
        else:
            return False
        