import discord
from appConfig import appConfig
import asyncio
from multiprocessing import Queue
from botCommand import botCommand
import emoji

#from discord.ext import commands
GuildMessageQue:Queue = None
CMDQue:Queue = None
BotToken:str = ""
DiscordClient:discord.client.Client= discord.Client()
GuildChatChannel = None
#DiscordClient:discord.client.Client = commands.Bot(command_prefix = '!')
def init(config: appConfig, cmdque:Queue , guildmessageque:Queue):
    global BotToken, GuildMessageQue, CMDQue
    BotToken = config.get("DISCORD", "bottoken", "")
    #DiscordClient.run(BotToken)
    GuildMessageQue = guildmessageque
    CMDQue = cmdque
    return

def getLoop():
    return DiscordClient.loop

def start():
    DiscordClient.run(BotToken)
    return

#THIS FILLS DiscordClient.guilds
@DiscordClient.event
async def on_ready():
    global GuildChatChannel
    print(f'{DiscordClient.user} has connected to Discord!')
    for guild in DiscordClient.guilds:
        print("I am connected to " + guild.name)
        GuildChatChannel = discord.utils.get(guild.text_channels, name="guild-chat")
    return

def eventNewDiscordMessage(sender:str, line:str):
    cmd : botCommand = botCommand()
    cmd.set(sender, "discord", line)
    CMDQue.put(cmd)
    return

@DiscordClient.event
async def on_message(message):
    if (GuildChatChannel is None or message.author.bot):
        return
    if(message.channel.id == GuildChatChannel.id):
        sender = message.author.nick if message.author.nick is not None else message.author.name
        mes:str = message.clean_content
        mes = emoji.demojize(mes)
        eventNewDiscordMessage(sender, mes)
    return

def botReply(message:str):

    return

async def startDiscordBot():
    await DiscordClient.start(BotToken)
    return

async def ProcessGuildMessageQue():
    global GuildMessageQue
    while True:
        junk = GuildMessageQue.qsize()
        if not GuildMessageQue.empty():
            try:
                cmd = GuildMessageQue.get_nowait()
                if(cmd.Sender == "Everquest"):
                    mes:str = emoji.emojize(cmd.Text)
                    await GuildChatChannel.send(mes)
                else:
                    await GuildChatChannel.send("<" + cmd.Sender + "> " + cmd.Text)
            except:
                print("Guild Message Que Get Error")
        else:
            await asyncio.sleep(2)    
        await asyncio.sleep(0)
    return