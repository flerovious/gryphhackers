from urllib.request import urlopen
import discord
from discord.ext import commands
import json
from urllib import response
import requests
import io


class Memes(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_meme(self):
        res = requests.get('https://meme-api.herokuapp.com/gimme/programmerhumor')
        json_data = json.loads(res.text)
        meme_url = json_data['url']
        return meme_url

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Memes load success.')

    # commands
    @commands.command()
    async def meme(self, ctx):
        print('Getting your meme')
        meme_url = self.get_meme()
        completed = False

        while not completed:
            try:
                meme = urlopen(meme_url).read()
                im = io.BytesIO(meme)
                await ctx.send(file=discord.File(im, "funny_meme.png"))
                completed = True
            except:
                print("running again")


def setup(client):
    client.add_cog(Memes(client))
