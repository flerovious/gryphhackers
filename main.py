import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix="!")

# database for would you rather questions
would_you_rather_qns = ['Would you rather have more time or more money?',  
'Would you rather have a rewind button or a pause button on your life?',
'Would you rather go to a movie or to dinner alone?', 'Would you rather go deep-sea diving or bungee jumping?',
'Would you rather be too busy or be bored?', 'Would you rather live where it is constantly winter or where it is constantly summer?',
'Would you rather have many good friends or one very best friend?'
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Would you rather game



@bot.command(pass_context=True)
async def wur_game(ctx):
    await ctx.send()

client.run(TOKEN)
