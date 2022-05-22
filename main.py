import os
import discord
import random 
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
my_tocken = 'OTc3NTYzOTMyODUwMDEyMjIx.G3932j.Zh89XDyAqw8zNSCFYhP_8FgESXKB45rXxX86ZE'

would_you_rather_qns = ['Would you rather have more time or more money?',  
    'Would you rather have a rewind button or a pause button on your life?',
    'Would you rather go to a movie or to dinner alone?', 'Would you rather go deep-sea diving or bungee jumping?',
    'Would you rather be too busy or be bored?', 'Would you rather live where it is constantly winter or where it is constantly summer?',
    'Would you rather have many good friends or one very best friend?'
    ]

bot = commands.Bot(command_prefix="/")

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

    if message.content.startswith('/wur'):
        await message.channel.send(would_you_rather_qns[random.randint(0, len(would_you_rather_qns) - 1)])

# Would you rather game
@commands.command()
async def wur_game():
    channel = bot.get_channel(977563932850012221)
    await channel.send(would_you_rather_qns[random.randint(0, len(would_you_rather_qns) - 1)])


bot.command()
async def test(ctx):
    await ctx.send("test")

bot.add_command(wur_game)

bot.run(my_tocken)
