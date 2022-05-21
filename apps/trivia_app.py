import typing
import requests

POINTS = 'points'
ANSWER = 'answer'
CATEGORY = 'category'
QUESTION = 'question'
RESULTS = 'results'
CORRECT = 'correct_answer'
INCORRECT = 'incorrect_answers'
DIFFICULTY = 'difficulty'


class TriviaApp:
    def __init__(self):
        self.scoreboard = {}
        self.questions = TriviaApp.fetch_questions(1)
        self.current_q = 0

    @staticmethod
    def fetch_questions(no_questions):
        r = requests.get(f'https://opentdb.com/api.php?amount={no_questions}&difficulty=easy&type=multiple')
        if r.status_code != 200:
            print('[TRIVIA APP] Failed getting questions')
        return r.json()[RESULTS]

    def get_difficulty(self):
        return self.questions[self.current_q][DIFFICULTY]

    def get_category(self):
        return self.questions[self.current_q][CATEGORY]

    def get_question(self):
        return self.questions[self.current_q][QUESTION]

    # todo: randomise
    def get_choices(self):
        return [self.questions[self.current_q][CORRECT]] + self.questions[self.current_q][INCORRECT]

    def get_participants(self):
        return self.scoreboard.keys()

    def get_rankings(self):
        return self.scoreboard.values()

    def add_points(self, user, points):
        self.scoreboard[user][POINTS] += points

    def get_points(self, user):
        return self.scoreboard[user][POINTS]

    def add_answer(self, user, answer):
        if self.scoreboard[user][ANSWER]:
            return False
        self.scoreboard[user][ANSWER] = answer

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
