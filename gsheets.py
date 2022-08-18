import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import re

SS:gspread.Spreadsheet = None
WS:gspread.Worksheet = None

def getFlagCell(name:str, flag:str) -> gspread.Cell:
    rowcell = WS.find(re.compile("(?i)^"+ name + "$"))
    colcell = WS.find(re.compile("(?i)^"+ flag + "$"))
    if rowcell is None or colcell is None:
        return None
    return WS.cell(rowcell.row, colcell.col)

def getFlagStatus(name:str, flag:str) -> bool:
    print("Try to get flag status for " + name + "for" + flag)
    cell:gspread.Cell = getFlagCell(name,flag)
    if(cell is None): return None
    return True if (cell.value == "TRUE") else False

def setFlagStatus(name:str, flag:str, value:bool) -> bool:
    cell:gspread.Cell = getFlagCell(name,flag)
    if(cell is None): return False
    WS.update_cell(cell.row, cell.col,"TRUE" if value else "FALSE")
    return True

def setFlagStatusAll(name:str, flag:str, count:int) -> bool:
    cell:gspread.Cell = getFlagCell(name,flag)
    if(cell is None): return False
    for i in range (5,cell.col+1):
        WS.update_cell(cell.row, i,"TRUE")
    return True

def init():
    global SS, WS
    #Authorize the API
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    file_name = 'python-sheet-oauth.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = gspread.authorize(creds)
    SS = client.open('GuildDoNProgression')
    WS = SS.get_worksheet(1)
    #setFlagStatus("Althea", "T1G",False)
    return


