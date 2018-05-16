import unittest

from ndimensionaltictactoe.models.round import Round


class TestRound(unittest.TestCase):
    def setUp(self):
        pass

    def test__init__round_points_are_larger_size_divided_by_three_and_multiplied_by_two_3(self):
        round = Round(3, 1, 3)
        self.assertEqual(2, round.winner_points)

    def test__init__round_points_are_larger_size_divided_by_three_and_multiplied_by_two_10(self):
        round = Round(10, 2, 3)
        self.assertEqual(6, round.winner_points)

    def test__init__round_points_are_larger_size_divided_by_three_and_multiplied_by_two_100(self):
        round = Round(100, 10, 3)
        self.assertEqual(66, round.winner_points)
