import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
#TOKEN = os.getenv('TOKEN')
token = 'OTc3NTYzOTMyODUwMDEyMjIx.G3932j.Zh89XDyAqw8zNSCFYhP_8FgESXKB45rXxX86ZE'

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f'Bot {client.user} is up and running.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#client.run(TOKEN)

client.run(token)
