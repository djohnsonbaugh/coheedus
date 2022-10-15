import json
from typing import List

from Models.API_RaidTick import ApiRaidTick


# {
#    "Name":"DefaultWithPoints",
#    "Ticks":[
#       {
#          "Description":"OnTime",
#          "Value":1,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"1945",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2000",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2015",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2030",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2045",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2100",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2115",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2130",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2145",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2200",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2215",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       },
#       {
#          "Description":"2230",
#          "Value":0.5,
#          "RaidId":33001036,
#          "TickId":null,
#          "Attendees":[
            
#          ]
#       }
#    ]
# }

class ApiRaidTemplate(object):

    def __init__(self, name):
        self.Name:str = name
        self.Ticks = []

    # @property
    # def Name(self)->str: return self.Name
    # @property
    # def Ticks(self)->List[ApiRaidTick]: return self.Ticks
    
   
    def from_json(self, json_str):
        self.Name:str = json_str["Name"]
        self.Ticks = []
        for row in json_str["Ticks"]:
            self.Ticks.append(ApiRaidTick().from_json(row))
        return self