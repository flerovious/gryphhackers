import discord
from discord.ext import commands, tasks
import time
from apps.trivia_app import TriviaApp, Difficulty
from enum import Enum

MINUTE = 30
E_ONE = "1️⃣"
E_TWO = "2️⃣"
E_THREE = "3️⃣"
E_FOUR = "4️⃣"


class GameState(Enum):
    START = 1,
    PLAYING = 2,
    ENDED = 3


# Function to create embed text
def embed_text(text, header="Trivia Bot", colour=discord.Color.blue()):
    em = discord.Embed(title=header, description=text, color=colour)
    return em


class Trivia(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.app = None
        self.deadline = None
        self.channel = None
        self.state = None
        self.posted = False

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia load success.')

    # On reaction to a trivia question
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.app and user in self.app.get_participants() and not self.app.get_answer(user):
            if reaction.emoji == E_ONE:
                self.app.add_answer(user, 0)
            elif reaction.emoji == E_TWO:
                self.app.add_answer(user, 1)
            if reaction.emoji == E_THREE:
                self.app.add_answer(user, 2)
            elif reaction.emoji == E_FOUR:
                self.app.add_answer(user, 3)
        if self.app and not user.bot:
            if reaction.emoji == "✅":
                self.app.add_participant(user)
                await self.channel.send(f"{user.mention} has joined")

    # commands
    @commands.command()
    async def trivia(self, ctx: commands.Context, *args):
        if "start" in args:
            if not self.game_start.is_running():
                self.app = TriviaApp(4, Difficulty.EASY)
                self.deadline = round(time.time()) + MINUTE
                self.channel = ctx.channel
                self.state = GameState.START
                self.game_start.start()
                em = discord.Embed(title="🕵️ Trivia 🕵️",
                                   description="Are you the brightest of them all?",
                                   color=discord.Color.green())
                em.add_field(name=f"Category", value=f"Any", inline=False)
                em.add_field(name="Difficulty", value=f"Easy", inline=False)
                em.add_field(name="Requested by", value=f"{ctx.message.author.mention}", inline=False)
                em.add_field(name="Game starting...", value=f'<t:{self.deadline}:R>', inline=False)
                message = await self.channel.send(embed=em, delete_after=MINUTE)
                await message.add_reaction("✅")
                return
            await ctx.send(embed=embed_text(f'Trivia has already started, please wait for the next round'))
        elif "end" in args:
            if self.game_start.is_running():
                self.game_end()
                await ctx.send(embed=embed_text(f'{ctx.message.author.mention} has ended Trivia'))
                return
            await ctx.send(embed=embed_text(f'Trivia Bot has not been started'))
        elif not args:
            em = discord.Embed(title="Help", color=discord.Color.blue())
            em.add_field(name=f"To start a game", value=f"Start with '!trivia start.'", inline=False)
            em.add_field(name="To join the game", value=f"Join with '!trivia join.'", inline=False)
            em.add_field(name="To end the game", value=f"End with '!trivia end.'", inline=False)
            await ctx.send(embed=em)
        else:
            # should use to log errors
            await ctx.send(embed=embed_text(f'Trivia fallthrough reached. ctx = {ctx}', header='Log'))

    def game_end(self):
        if self.game_start.is_running():
            self.app = None
            self.deadline = None
            if self.game_start.is_running():
                self.game_start.cancel()

    async def post_question(self):
        self.deadline = round(time.time()) + MINUTE
        question = self.app.get_question()
        category = self.app.get_category()
        choices = self.app.get_choices()
        # send question to channel
        em = discord.Embed(title="❔ Trivia Question ❔", description=question, color=discord.Color.green())
        em.add_field(name=f"Category", value=f"{category}", inline=False)
        em.add_field(name="Difficulty", value=f"{'Easy'}", inline=False)
        for i, choice in enumerate(choices):
            em.add_field(name=f"Option {i + 1}", value=choice, inline=False)
        em.add_field(name="Time left", value=f'<t:{self.deadline}:R>', inline=False)
        message = await self.channel.send(embed=em, delete_after=MINUTE)
        await message.add_reaction(E_ONE)
        await message.add_reaction(E_TWO)
        await message.add_reaction(E_THREE)
        await message.add_reaction(E_FOUR)

    # background tasks
    @tasks.loop(seconds=1)
    async def game_start(self):
        if self.state == GameState.START and time.time() >= self.deadline:
            print('game start')
            await self.post_question()
            self.state = GameState.PLAYING
        if self.state == GameState.PLAYING:
            if self.app.has_all_answered() or time.time() > self.deadline:
                results = self.app.verify()
                ranking = self.app.get_rankings()
                em = discord.Embed(title=f"🔥 Round {self.app.current_q} 🔥", color=discord.Color.green())
                for (index, (user, points)) in enumerate(ranking):
                    mark = "✅" if results[user] else "❌"
                    em.add_field(name=f"Rank {index + 1}: {points} points", value=f"{mark}\t{user}", inline=False)
                await self.channel.send(embed=em, delete_after=MINUTE)

                if self.app.has_ended():
                    self.state = GameState.ENDED
                else:
                    await self.post_question()
                    print(self.app.get_correct())

        if self.state == GameState.ENDED:
            print('has ended')
            em = discord.Embed(title="🏆 Leaderboard 🏆", description="Game Over!", color=discord.Color.green())
            ranking = self.app.get_rankings()
            for (index, (user, points)) in enumerate(ranking):
                em.add_field(name=f"Rank {index + 1}: {points} points", value=f"{user}", inline=False)
            await self.channel.send(embed=em, delete_after=MINUTE)
            self.game_end()


def setup(client):
    client.add_cog(Trivia(client))
