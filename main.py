import os
# import discord
import random 
# from dotenv import load_dotenv
from discord.ext import commands
import json
from urllib import response
import requests

# load_dotenv()
# TOKEN = os.getenv('TOKEN')
token = 'OTc3NTYzOTMyODUwMDEyMjIx.G3932j.Zh89XDyAqw8zNSCFYhP_8FgESXKB45rXxX86ZE'
bot = commands.Bot(command_prefix="!")

# bot comes online
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# Would you rather game
@bot.command()
async def wur_game(ctx):
    print('Game in session')
    response = requests.get('https://would-you-rather-api.abaanshanid.repl.co')
    json_data = json.loads(response.text)
    question = json_data['data']
    await ctx.send(question)

bot.run(token)
