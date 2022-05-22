import discord
from discord.ext import commands
import requests
import random
import html
from apps.trivia_app import *


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

        # Sets colour of embed sidebar based on difficulty
        def set_difficulty_colour(difficulty):
            if difficulty == 'easy':
                return 0x2eff00  # green
            elif difficulty == 'medium':
                return 0xdc7633  # orange
            else:
                return 0xff0000  # red

        # TODO -- HOW TO SET
        number_qn = 1
        difficulty_choice = Difficulty('easy')

        # Creates instance of trivia and assigns variables for embed
        trivia_inst = TriviaApp(no_questions=number_qn, difficulty=difficulty_choice)
        category = trivia_inst.get_category()
        difficulty = trivia_inst.get_difficulty()
        colour = set_difficulty_colour(difficulty)
        question = trivia_inst.get_question()
        answers = trivia_inst.get_choices()

        # Sets them to a certain multiple choice
        answer_dict = {}
        for count, choice in enumerate(['A', 'B', 'C', 'D']):
            answer_dict[choice] = answers[count]

        # Embed design
        em = discord.Embed(title="Trivia Question \u2753", description=question, color=colour)
        em.add_field(name=f"Category", value=f"{category}", inline=False)
        em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=False)
        em.add_field(name="A", value=f"{answer_dict['A']}", inline=False)
        em.add_field(name="B", value=f"{answer_dict['B']}", inline=False)
        em.add_field(name="C", value=f"{answer_dict['C']}", inline=False)
        em.add_field(name="D", value=f"{answer_dict['D']}", inline=False)
        react_msg = await ctx.send(embed=em)
        await react_msg.add_reaction('\U0001f1e6')
        await react_msg.add_reaction('\U0001f1e7')
        await react_msg.add_reaction('\U0001f1e8')
        await react_msg.add_reaction('\U0001f1e9')


def setup(client):
    client.add_cog(Trivia(client))
