import discord
from discord.ext import commands
import requests
import random
import html


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

        def get_question():
            r = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
            assert r.status_code == 200
            data = r.json()['results'][0]
            return data

        data = get_question()
        # Assigns variables
        category, correct_answer, difficulty, incorrect_answers, question, qn_type = data['category'], data[
            'correct_answer'], data['difficulty'], data['incorrect_answers'], data['question'], data['type']

        # Sets colour of embed based on difficulty
        if difficulty == 'easy':
            colour = 0x2eff00  # green
        elif difficulty == 'medium':
            colour = 0xdc7633  # orange
        else:
            colour = 0xff0000  # red

        # Randomises answers and sets them to a certain multiple choice
        answer_list = [correct_answer] + incorrect_answers
        random.shuffle(answer_list)
        answer_dict = {}
        for count, choice in enumerate(['A', 'B', 'C', 'D']):
            answer_dict[choice] = answer_list[count]

        # Embed design
        em = discord.Embed(title="Trivia Question \u2753", description=question, color=colour)
        em.add_field(name=f"Category", value=f"{category}", inline=False)
        em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=False)
        em.add_field(name="A", value=f"{answer_dict['A']}", inline=True)
        em.add_field(name="B", value=f"{answer_dict['B']}", inline=True)
        em.add_field(name="\u200b", value="\u200b", inline=True)
        em.add_field(name="C", value=f"{answer_dict['C']}", inline=True)
        em.add_field(name="D", value=f"{answer_dict['D']}", inline=True)
        em.add_field(name="\u200b", value="\u200b", inline=True)
        react_msg = await ctx.send(embed=em)
        await react_msg.add_reaction('\U0001f1e6')
        await react_msg.add_reaction('\U0001f1e7')
        await react_msg.add_reaction('\U0001f1e8')
        await react_msg.add_reaction('\U0001f1e9')


def setup(client):
    client.add_cog(Trivia(client))
