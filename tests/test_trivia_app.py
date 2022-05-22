import unittest
from apps.trivia_app import TriviaApp, Difficulty


class TestTriviaApp(unittest.TestCase):
    def setUp(self) -> None:
        self.users = ["user 1", "user 2"]
        self.app = TriviaApp(1, Difficulty.EASY)

    def tearDown(self) -> None:
        self.app = None

    def test_add_participant(self):
        for user in self.users:
            self.app.add_participant(user)
            self.assertIn(user, self.app.get_participants())

    def test_add_points(self):
        for user in self.users:
            self.app.add_participant(user)

        for user in self.users:
            self.assertEqual(self.app.get_points(user), 0)

        self.app.add_points(self.users[0], 1)
        for user in self.users:
            points = self.app.get_points(user)
            if user == self.users[0]:
                self.assertEqual(points, 1)
            else:
                self.assertEqual(points, 0)

    def test_answer(self):
        for index, user in enumerate(self.users):
            self.app.add_participant(user)
            self.assertIsNone(self.app.get_answer(user))

            self.app.add_answer(user, index)
            self.assertEqual(self.app.get_answer(user), index)

    def test_points(self):
        for user in self.users:
            self.app.add_participant(user)
            self.assertEqual(self.app.get_points(user), 0)

            self.app.add_points(user, 1)
            self.assertEqual(self.app.get_points(user), 1)

    def test_verify(self):
        self.assertFalse(self.app.has_ended())

        correct_user = self.users[0]
        correct_answer = self.app.get_correct()
        for index, user in enumerate(self.users):
            self.app.add_participant(user)
            if user == correct_user:
                self.app.add_answer(user, correct_answer)
            else:
                self.app.add_answer(user, correct_answer + 1)

        self.app.verify()
        for user in self.users:
            points = self.app.get_points(user)
            if user == correct_user:
                self.assertEqual(points, 1)
            else:
                self.assertEqual(points, 0)

        self.assertTrue(self.app.has_ended())


if __name__ == '__main__':
    unittest.main()
