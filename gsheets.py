import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

SS:gspread.Spreadsheet = None
WS:gspread.Worksheet = None

def getFlagCell(name:str, flag:str) -> gspread.Cell:
    row = 1
    col = 1
    for row in range (1,WS.row_count):
        data = WS.cell(row,col).value
        if data == "Name":
            break
        row += 1
    for col in range (1,WS.col_count):
        data = WS.cell(row,col).value
        if data == flag:
            break
        col += 1
    for row in range (row +1 ,WS.row_count):
        data = WS.cell(row,1).value
        if data == name:
            return WS.cell(row,col)
        row += 1
    return None

def getFlagStatus(name:str, flag:str) -> bool:
    cell:gspread.Cell = getFlagCell(name,flag)
    if(cell is None): return False
    return True if (cell.value == "TRUE") else False

def setFlagStatus(name:str, flag:str, value:bool) -> bool:
    cell:gspread.Cell = getFlagCell(name,flag)
    if(cell is None): return False
    WS.update_cell(cell.row, cell.col,"TRUE" if value else "FALSE")
    return True

def init():
    global SS, WS
    #Authorize the API
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    file_name = 'python-sheet-358820-d8c07e7ce346.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = gspread.authorize(creds)
    SS = client.open('GuildDoNProgression')
    WS = SS.get_worksheet(1)
    #setFlagStatus("Althea", "T1G",False)
    return


