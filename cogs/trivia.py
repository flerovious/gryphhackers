import discord
from discord.ext import commands, tasks
import requests
import random
import time
from apps.trivia_app import TriviaApp, Difficulty
from enum import Enum

MINUTE = 10


class GameState(Enum):
    START = 1,
    PLAYING = 2,
    ENDED = 3


class Trivia(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.app = None
        self.start_time = None
        self.channel = None
        self.state = None

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia load success.')

    # commands
    @commands.command()
    async def trivia(self, ctx: commands.Context, *args):
        if "start" in args:
            if not self.start_time and not self.game_start.is_running():
                self.app = TriviaApp(4, Difficulty.EASY)
                self.start_time = round(time.time()) + MINUTE
                self.channel = ctx.channel
                self.state = GameState.START
                self.game_start.start()
                await ctx.send(f'Trivia starting in <add countdown>')
                return
            if round(time.time()) < self.start_time:
                await ctx.send(f'Trivia already in progress. Join now with <add join sub command>')
                return
            await ctx.send(f'Trivia has already started, please wait for the next round')
        elif "join" in args:
            if round(time.time()) < self.start_time:
                if ctx.message.author.id in self.app.get_participants():
                    await ctx.send(f"You're already in Trivia")
                    return
                self.app.add_participant(ctx.message.author.id)
                await ctx.send(f'You have joined the Trivia')
                return
            await ctx.send(f'Trivia has already started, please wait for the next round')
        elif "end" in args:
            if self.start_time:
                self.game_end()
                await ctx.send(f'{ctx.message.author.mention} has ended Trivia')
                return
            await ctx.send(f'TriviaApp has not been started')
        elif not args:
            await ctx.send(f'Help message')
        else:
            # should use to log errors
            await ctx.send(f'Trivia fallthrough reached. ctx = {ctx}')

    def game_end(self):
        if self.start_time:
            self.app = None
            self.start_time = None
            if self.game_start.is_running():
                self.game_start.cancel()

    # background tasks
    @tasks.loop(seconds=1)
    async def game_start(self):
        if self.state == GameState.START and time.time() >= self.start_time:
            print('game start')
            self.state = GameState.PLAYING
            question = self.app.get_question()
            category = self.app.get_question()
            choices = self.app.get_choices()
            # send question to channel
            print(f'sending question {question}')
        if self.state == GameState.PLAYING:
            if self.app.has_all_answered() or time.time() > self.start_time + (self.app.current_q + 1) * MINUTE:
                results = self.app.verify()
                ranking = self.app.get_rankings()
                print(ranking)
                for user, is_correct in results:
                    points = self.app.get_points(user)
                    if is_correct:
                        # send message to user that they are correct, total points and ranking
                        pass
                    else:
                        # send message to user that they are incorrect, total points and ranking
                        print(f'{user} was incorrect')
                        pass
            if not self.app.has_ended():
                question = self.app.get_question()
                category = self.app.get_question()
                choices = self.app.get_choices()
                # send question to channel
                print(f'sending question {question}')
            else:
                self.state = GameState.ENDED
        if self.state == GameState.ENDED:
            print('has ended')
            self.game_end()
            # send message to all that game has ended

        # data = get_question()
        # # Assigns variables
        # category, correct_answer, difficulty, incorrect_answers, question, qn_type = data['category'], data[
        #     'correct_answer'], data['difficulty'], data['incorrect_answers'], data['question'], data['type']
        #
        # # Sets colour of embed based on difficulty
        # if difficulty == 'easy':
        #     colour = 0x2eff00  # green
        # elif difficulty == 'medium':
        #     colour = 0xdc7633  # orange
        # else:
        #     colour = 0xff0000  # red
        # # Sets colour of embed sidebar based on difficulty
        # def set_difficulty_colour(difficulty):
        #     if difficulty == 'easy':
        #         return 0x2eff00  # green
        #     elif difficulty == 'medium':
        #         return 0xdc7633  # orange
        #     else:
        #         return 0xff0000  # red
        #
        # # TODO -- HOW TO SET
        # number_qn = 1
        # difficulty_choice = Difficulty('easy')
        #
        # # Creates instance of trivia and assigns variables for embed
        # trivia_inst = TriviaApp(no_questions=number_qn, difficulty=difficulty_choice)
        # category = trivia_inst.get_category()
        # difficulty = trivia_inst.get_difficulty()
        # colour = set_difficulty_colour(difficulty)
        # question = trivia_inst.get_question()
        # answers = trivia_inst.get_choices()
        #
        # # Sets them to a certain multiple choice
        # answer_dict = {}
        # for count, choice in enumerate(['A', 'B', 'C', 'D']):
        #     answer_dict[choice] = answers[count]
        #
        # # Embed design
        # em = discord.Embed(title="Trivia Question \u2753", description=question, color=colour)
        # em.add_field(name=f"Category", value=f"{category}", inline=False)
        # em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=False)
        # em.add_field(name="A", value=f"{answer_dict['A']}", inline=False)
        # em.add_field(name="B", value=f"{answer_dict['B']}", inline=False)
        # em.add_field(name="C", value=f"{answer_dict['C']}", inline=False)
        # em.add_field(name="D", value=f"{answer_dict['D']}", inline=False)
        # react_msg = await ctx.send(embed=em)
        # await react_msg.add_reaction('\U0001f1e6')
        # await react_msg.add_reaction('\U0001f1e7')
        # await react_msg.add_reaction('\U0001f1e8')
        # await react_msg.add_reaction('\U0001f1e9')


def setup(client):
    client.add_cog(Trivia(client))
