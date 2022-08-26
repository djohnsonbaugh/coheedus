########################################
#All Everquest Application Interaction
########################################
import winOS
import time
import pyperclip
from winOS import winKey
import appConfig
from multiprocessing import Queue
from botCommand import botCommand
from datetime import datetime, timedelta

#Global Initialization
EQWindowName:str = "EverQuest"
PasteKey:winKey = winKey.kV
PasteKeyShift:bool = False
PasteKeyCtrl:bool = True
PasteKeyAlt:bool = False
EQMessageQue:Queue=None
EQMessageVerificationQue:Queue=None
PlayerName = ""
def init(config: appConfig, eqmessage:Queue, eqmessageverify:Queue):
    global EQWindowName,EQMessageQue,EQMessageVerificationQue, PlayerName
    global PasteKey, PasteKeyCtrl, PasteKeyShift, PasteKeyAlt
    EQWindowName = config.get("EVERQUEST", "appName", EQWindowName)
    pkey:str = config.get("EVERQUEST","pasteKey", PasteKey.name)
    PasteKey = winKey[pkey]
    PasteKeyCtrl = config.getBool("EVERQUEST","pasteKeyCtrl", PasteKeyCtrl)
    PasteKeyShift = config.getBool("EVERQUEST","pasteKeyShift", PasteKeyShift)
    PasteKeyAlt = config.getBool("EVERQUEST","pasteKeyAlt", PasteKeyAlt)
    EQMessageQue= eqmessage
    EQMessageVerificationQue = eqmessageverify
    PlayerName = config.get("EVERQUEST", "character", "Coheedus")
    return
     

def isEQActive() ->bool:
    return (winOS.getActiveWindow() == EQWindowName)

def activateEQ() ->bool:
    return winOS.actviateFirstWindow(EQWindowName)

#Copies command to clipboard and pastes it into EQ (assumes EQ is the active window -> use enterCommandSafe)
def enterCommand(command:str) -> bool:
    pyperclip.copy(command)
#    winOS.pushKey(winKey.Down, True)
#    time.sleep(.1)
#    winOS.pushKey(winKey.Enter)
#    time.sleep(.1)
    winOS.pushKey(winKey.Enter)
    time.sleep(.1)
    winOS.pushKey(PasteKey, PasteKeyShift, PasteKeyCtrl, PasteKeyAlt)
    time.sleep(.1)
    winOS.pushKey(winKey.Enter)
    return True

def resetCursor(command:str) -> bool:
    winOS.pushKey(winKey.Down, True)
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

def sendMessage(chan: str, message: str):
    command = "/" + chan + " " + message
    enterCommandSafe(command, True)
    return

def tell(name: str, message: str):
    sendMessage("tell " + name, message)
    return

def runEQMessagePaster():
    messages = []
    inerror = 0
    while winOS.isParentAlive():
        if inerror >= 4:
            print("cursor reset...")
            winOS.toggleWindowForFunction(EQWindowName, resetCursor, "")
            inerror = 0
        elif not EQMessageVerificationQue.empty():
            chan = ""
            cmd:botCommand = None
            unfoundmessages = []
            try:
                cmd = EQMessageVerificationQue.get_nowait()
            except:
                print("EQ Message Verify Que Get Error: " + str(cmd))
            if cmd is not None:
                print("verifing message: " + str(cmd))
                found = False
                for chan,message,d in messages:
                    if cmd.Text is None:
                        #print("found bad message does '" + "tell " + cmd.Sender.lower() + "!=" +  chan.lower())
                        if "tell " + cmd.Sender.lower() != chan.lower():
                            unfoundmessages.append((chan,message,d))
                        else:
                            inerror = 0
                            found = True
                            print("message verified but NOT ONLINE!!!: " + chan + "->" + message + "(" + str(d) + ")")
                    elif cmd.Text.strip() != message.strip() or found:
                        #print("failed match:'" + cmd.Text + "!=" +  message)
                        unfoundmessages.append((chan,message,d))
                    else:
                        inerror = 0
                        found = True
                        print("message verified!!!: " + chan + "->" + message + "(" + str(d) + ")")
                messages = unfoundmessages
        elif not EQMessageQue.empty():
            chan = ""
            try:
                chan,message = EQMessageQue.get_nowait()
            except:
                print("EQ Message Que Get Error: " + str(cmd))
            if chan != "":
                #skip tells to myself
                if chan.lower() == "tell " + PlayerName.lower():
                    continue
                sendMessage(chan,message)
                d = datetime.now()
                messages.append((chan,message,d))
                print("added eq message: " + chan + "->" + message + "(" + str(d) + ")")
        elif len(messages) > 0:
            unfoundmessages = []
            for chan,message,d in messages:
                if datetime.now() -d > timedelta(seconds=5):
                    EQMessageQue.put((chan,message))
                    print("message retry!!!: " + chan + "->" + message)
                    inerror += 1
                else:
                    unfoundmessages.append((chan,message,d))
                messages = unfoundmessages
        else:
            time.sleep(2)
    print("Auc parent dead - goodbye")
    return