import unittest
from copy import deepcopy
from uuid import uuid4

from apscheduler.events import JobExecutionEvent
from mock import patch, MagicMock

from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.models.round import Round
from ndimensionaltictactoe.models.tournament import Tournament


class TestTournament(unittest.TestCase):
    def setUp(self):
        self.player_1 = Player(uuid4(), "player 1", "update_url1")
        self.player_2 = Player(uuid4(), "player 2", "update_url2")
        self.player_3 = Player(uuid4(), "player 3", "update_url3")

        self.game_1 = Game("Test Game 1", uuid4(), deepcopy(self.player_1), deepcopy(self.player_2))
        self.game_2 = Game("Test Game 2", uuid4(), deepcopy(self.player_1), deepcopy(self.player_3))
        self.game_3 = Game("Test Game 3", uuid4(), deepcopy(self.player_2), deepcopy(self.player_3))

    @patch('ndimensionaltictactoe.models.tournament.game_thread', autospec=True)
    def test__play_round__calls_game_thread_once_when_two_players_in_lobby(self, mock_game_thread):
        lobby = {self.player_1.key: self.player_1,
                 self.player_2.key: self.player_2}

        tournament = Tournament(uuid4(), "Test Tournament", lobby)

        round = Round(3, 3, 3)

        tournament.play_round(round)

        self.assertEqual(1, len(tournament.rounds[0].games))

    @patch('ndimensionaltictactoe.models.tournament.game_thread', autospec=True)
    def test__play_round__calls_game_thread_thrice_when_three_players_in_lobby(self, mock_game_thread):
        lobby = {self.player_1.key: self.player_1,
                 self.player_2.key: self.player_2,
                 self.player_3.key: self.player_3}

        tournament = Tournament(uuid4(), "Test Tournament", lobby)

        round = Round(3, 3, 3)

        tournament.play_round(round)

        self.assertEqual(3, len(tournament.rounds[0].games))

    def test__play_round__throws_exception_when_round_is_already_in_progress(self):
        pass

    def test__process_completed_game__calculates_points_for_two_players(self):
        round = Round(3, 3, 3)
        round.games = [self.game_1]
        tournament = Tournament(uuid4(), "Test Tournament", [])
        tournament.rounds.append(round)
        tournament.current_round = round
        tournament.games_in_progress = [self.game_1.key]

        self.game_1.player_x.winner = True
        self.game_1.player_o.winner = False

        tournament.process_completed_game()

        self.assertEqual(2, tournament.rounds[0].scoreboard[self.player_1.key])
        self.assertEqual(0, tournament.rounds[0].scoreboard[self.player_2.key])

    def test__process_completed_game__calculates_points_for_three_players(self):
        round = Round(10, 10, 3)

        self.game_1.player_x.winner = False
        self.game_1.player_o.winner = False

        self.game_2.player_x.winner = True
        self.game_2.player_o.winner = False

        self.game_3.player_x.winner = False
        self.game_3.player_o.winner = True

        round.games = [self.game_1, self.game_2, self.game_3]
        tournament = Tournament(uuid4(), "Test Tournament", [])
        tournament.rounds.append(round)
        tournament.current_round = round
        tournament.games_in_progress = [self.game_1.key]

        event = JobExecutionEvent(1234, 4567, 'jobstore', 'whenever', retval=self.game_1)

        tournament.process_completed_game()

        self.assertEqual(9, tournament.rounds[0].scoreboard[self.player_1.key])
        self.assertEqual(3, tournament.rounds[0].scoreboard[self.player_2.key])
        self.assertEqual(6, tournament.rounds[0].scoreboard[self.player_3.key])

    def test__get_scoreboard__returns_total_points_for_each_player(self):
        round_1 = Round(0, 0, 0)
        round_2 = Round(0, 0, 0)
        round_3 = Round(0, 0, 0)
        round_1.scoreboard = {self.player_1.key: 1, self.player_2.key: 2}
        round_2.scoreboard = {self.player_1.key: 3, self.player_2.key: 4}
        round_3.scoreboard = {self.player_1.key: 5, self.player_2.key: 6}
        tournament = Tournament(uuid4(), "Test Tournament", [])
        tournament.rounds = [round_1, round_2, round_3]

        tournament_scoreboard = tournament.get_scoreboard()

        self.assertEqual(9, tournament_scoreboard[self.player_1.key])
        self.assertEqual(12, tournament_scoreboard[self.player_2.key])
