import os
# import discord
import random 
# from dotenv import load_dotenv
from discord.ext import commands

# load_dotenv()
# TOKEN = os.getenv('TOKEN')

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
    would_you_rather_qns = ['Would you rather have more time or more money?',  
    'Would you rather have a rewind button or a pause button on your life?',
    'Would you rather go to a movie or to dinner alone?', 'Would you rather go deep-sea diving or bungee jumping?',
    'Would you rather be too busy or be bored?', 'Would you rather live where it is constantly winter or where it is constantly summer?',
    'Would you rather have many good friends or one very best friend?'
    ]
    await ctx.send(f'{random.choice(would_you_rather_qns)}')

bot.run('TOKEN')
