from lxml import html
import requests

class wishlist(object):
    """description of class"""


    def __init__(self, owner:str, id:str):
        self.Owner = owner
        self.ID = id
        self.Character = ""
        self.Items = []
        self.Initialized = False
        return

    def Initialize(self)->bool:
        page = requests.get('https://www.raidloot.com/profile/' + self.ID)
        if(page.status_code != 200):
            return False
        tree = html.fromstring(page.content)
        self.Character = tree.xpath('//*[@id="item0"]/span[1]')[0].text
        self.Items = []
        for i in range(1,1000):
            path = '/html/body/div[1]/div/section[1]/div[2]/div[2]/div/div[' + str(i) + ']/img'
            if tree.xpath(path):
                self.Items.append(tree.xpath(path)[0].attrib['title'])
            else:
                break
        self.Initialized = True
        return True

    def Wants(self,item:str) -> bool:
        return (item in self.Items)