import discord
from discord.ext import commands


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.isStarted = False

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia load success.')

    # commands
    @commands.command()
    async def trivia(self, ctx, *args):
        if "start" in args:
            # todo: start
            pass
        elif "join" in args:
            # todo: add participant
            pass
        elif "end" in args:
            # todo: end
            pass
        elif not args:
            # todo: help message on usage
            await ctx.send(f'Help message')
        else:
            # should use to log errors
            await ctx.send(f'Trivia fallthrough reached. ctx = {ctx}')


def setup(client):
    client.add_cog(Trivia(client))
