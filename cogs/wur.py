import discord
from discord.ext import commands
import json
from urllib import response
import requests


class WUR(commands.Cog):
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Would You Rather load success.')

    # commands
    @commands.command()
    async def wur(self, ctx):
        print('Game in session')
        res = requests.get('https://would-you-rather-api.abaanshanid.repl.co')
        json_data = json.loads(res.text)
        question = json_data['data']
        lightbulb_emoji = '\uD83D\uDCA1'
        embed_qn = discord.Embed(
            title=f'{lightbulb_emoji} {question}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_qn)
        # await ctx.send(f'{question}')


def setup(client):
    client.add_cog(WUR(client))
