from enum import Enum
import requests
import random
import html

POINTS = 'points'
ANSWER = 'answer'
CATEGORY = 'category'
QUESTION = 'question'
RESULTS = 'results'
CORRECT = 'correct_answer'
INCORRECT = 'incorrect_answers'
DIFFICULTY = 'difficulty'
CHOICES = 'choices'


class Difficulty(str, Enum):
    EASY = 'easy',
    MEDIUM = 'medium',
    HARD = 'hard',


class TriviaApp:
    def __init__(self, no_questions: int, difficulty: Difficulty):
        self.scoreboard = {}
        self.questions = TriviaApp.fetch_questions(no_questions, difficulty)
        self.current_q = 0

    @staticmethod
    def fetch_questions(no_questions, difficulty):
        url = f'https://opentdb.com/api.php' \
              f'?amount={no_questions}' \
              f'&difficulty={difficulty.value}' \
              f'&type=multiple'
        r = requests.get(url)
        if r.status_code != 200:
            print('[TRIVIA APP] Failed getting questions')
        body = r.json()[RESULTS]
        questions = []
        for data in body:
            correct = html.unescape(data[CORRECT])
            choices = [correct] + data[INCORRECT]
            random.shuffle(choices)
            question = {
                QUESTION: html.unescape(data[QUESTION]),
                CATEGORY: html.unescape(data[CATEGORY]),
                DIFFICULTY: html.unescape(data[DIFFICULTY]),
                CHOICES: [html.unescape(choice) for choice in choices],
                CORRECT: choices.index(correct)
            }
            questions.append(question.copy())
        return questions

    def get_difficulty(self):
        return self.questions[self.current_q][DIFFICULTY]

    def get_category(self):
        return self.questions[self.current_q][CATEGORY]

    def get_question(self):
        return self.questions[self.current_q][QUESTION]

    def get_choices(self):
        return self.questions[self.current_q][CHOICES]

    def get_correct(self):
        return self.questions[self.current_q][CORRECT]

    def get_participants(self):
        return self.scoreboard.keys()

    def get_rankings(self):
        return self.scoreboard.values()

    def add_points(self, user, points):
        self.scoreboard[user][POINTS] += points

    def get_points(self, user):
        return self.scoreboard[user][POINTS]

    def add_answer(self, user, answer: int):
        if self.scoreboard[user][ANSWER]:
            return False
        self.scoreboard[user][ANSWER] = answer
        return True

    def get_answer(self, user):
        return self.scoreboard[user][ANSWER]

    def clear_answer(self, user):
        self.scoreboard[user][ANSWER] = None

    # check answers of all participants and add points accordingly
    def verify(self):
        if self.current_q < len(self.questions):
            correct_answer = self.questions[self.current_q][CORRECT]
            for user in self.scoreboard:
                if self.get_answer(user) == correct_answer:
                    self.add_points(user, 1)
                self.clear_answer(user)
            self.current_q += 1
            return True
        return False

    def has_ended(self):
        return self.current_q >= len(self.questions)

    def add_participant(self, user: str) -> None:
        self.scoreboard[user] = {
            POINTS: 0,
            ANSWER: None
        }
