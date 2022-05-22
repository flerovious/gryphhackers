import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
#TOKEN = os.getenv('TOKEN')
token = 'OTc3NTUyODc5NzkzNjAyNTgw.GTEOxr.G7cxfCRwvXfASb3vuBlHX9RtGWYaY1_cFutGZE'

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f'Bot {client.user} is up and running.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#client.run(TOKEN)

client.run(token)
