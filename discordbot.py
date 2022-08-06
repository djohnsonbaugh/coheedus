import discord
from appConfig import appConfig
import asyncio
#from discord.ext import commands

BotToken:str = ""
DiscordClient:discord.client.Client = discord.Client()
GuildChatChannel = None
NewMessageCallback = None
#DiscordClient:discord.client.Client = commands.Bot(command_prefix = '!')
def init(config: appConfig, newmessagecallback):
    global BotToken, NewMessageCallback
    BotToken = config.get("DISCORD", "bottoken", "")
    NewMessageCallback = newmessagecallback
    #DiscordClient.run(BotToken)
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

@DiscordClient.event
async def on_message(message):
    if (GuildChatChannel is None or message.author.bot):
        return
    if(message.channel.id == GuildChatChannel.id):
        sender = message.author.nick if message.author.nick is not None else message.author.name
        NewMessageCallback(sender, message.content.encode('utf8').decode("utf-8"))
    return

def botReply(message:str):

    return

async def newGuildMessageEvent(sender:str, message:str):
    await GuildChatChannel.send("<" + sender + "> " + message)   
    return


async def startDiscordBot():
    await DiscordClient.start(BotToken)
    return