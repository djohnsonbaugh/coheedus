########################################
#All OS Interaction
########################################

import win32gui
import win32con
import win32api
import time
from enum import Enum

class winKey(Enum):
    LM = 0x01
    RM = 0x02
    Tab = 0x09
    Enter = 0x0D
    Space = 0x20
    PageUp = 0x21
    PageDn = 0x22
    End = 0x23
    Home = 0x24
    Left = 0x25
    Up = 0x26
    Right = 0x27
    Down = 0x28
    k0 = 0x30
    k1 = 0x31
    k2 = 0x32
    k3 = 0x33
    k4 = 0x34
    k5 = 0x35
    k6 = 0x36
    k7 = 0x37
    k8 = 0x38
    k9 = 0x39
    kA = 0x41
    kB = 0x42
    kC = 0x43
    kD = 0x44
    kE = 0x45
    kF = 0x46
    kG = 0x47
    kH = 0x48
    kI = 0x49
    kJ = 0x4A
    kK = 0x4B
    kL = 0x4C
    kM = 0x4D
    kN = 0x4E
    kO = 0x4F
    kP = 0x50
    kQ = 0x51
    kR = 0x52
    kS = 0x53
    kT = 0x54
    kU = 0x55
    kV = 0x56
    kW = 0x57
    kX = 0x58
    kY = 0x59
    kZ = 0x5A
    n0 = 0x60
    n1 = 0x61
    n2 = 0x62
    n3 = 0x63
    n4 = 0x64
    n5 = 0x65
    n6 = 0x66
    n7 = 0x67
    n8 = 0x68
    n9 = 0x69
    nMul = 0x6A
    nAdd = 0x6B
    nMin = 0x6D
    nDec = 0x6E
    nDiv = 0x6F
    F1   = 0x70
    F2   = 0x71
    F3   = 0x72
    F4   = 0x73
    F5   = 0x74
    F6   = 0x75
    F7   = 0x76
    F8   = 0x77
    F9   = 0x78
    F10  = 0x79
    F11  = 0x7A
    F12  = 0x7B
    FSlash = 0xBF

def pushKey(keypress: winKey, shift: bool=False, ctrl: bool=False, alt: bool=False):

    if shift:
        win32api.keybd_event(0x10, win32api.MapVirtualKey(0x10, 0), 0, 0)
    if ctrl:
        win32api.keybd_event(0x11, win32api.MapVirtualKey(0x11, 0), 0, 0)
    if alt:
        win32api.keybd_event(0x12, win32api.MapVirtualKey(0x12, 0), 0, 0)

    # wait for it to get registered. 
    # You might need to increase this time for some applications
    time.sleep(.05)

    # send key down event
    win32api.keybd_event(keypress.value, win32api.MapVirtualKey(keypress.value, 0), 0, 0)

    # wait for it to get registered. 
    # You might need to increase this time for some applications
    time.sleep(.1)

    # send key up event
    win32api.keybd_event(keypress.value, win32api.MapVirtualKey(keypress.value, 0), win32con.KEYEVENTF_KEYUP, 0)

    if shift:
        win32api.keybd_event(0x10, win32api.MapVirtualKey(0x10, 0), win32con.KEYEVENTF_KEYUP, 0)
    if ctrl:
        win32api.keybd_event(0x11, win32api.MapVirtualKey(0x11, 0), win32con.KEYEVENTF_KEYUP, 0)
    if alt:
        win32api.keybd_event(0x12, win32api.MapVirtualKey(0x12, 0), win32con.KEYEVENTF_KEYUP, 0)

    return

def getActiveWindow() -> str:
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def getWindowHandles(name:str) -> [int]:
    hwnds:[int] = []
    def findhwnd(hwnd,ctx):
        if win32gui.GetWindowText(hwnd) == name: # check the title
            hwnds.append(hwnd)

    win32gui.EnumWindows(findhwnd,None)
    return hwnds

def actviateFirstWindow(name:str) -> bool:
    for hwnd in getWindowHandles(name):
        return activateWindow(hwnd)

def activateWindow(hwnd:int) ->bool:
    try:
        return win32gui.SetForegroundWindow(hwnd)
    except:
        return False

def toggleWindowForFunction(winName:str, func, arg):
    hwnd:int = win32gui.GetForegroundWindow()
    actviateFirstWindow(winName)
    for i in range(0,100):
        if(self.getActiveWindow() == winName) : break
        time.sleep(.05)
    ret = func(arg)
    activateWindow(hwnd)
    return ret