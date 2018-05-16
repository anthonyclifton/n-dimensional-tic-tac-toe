import unittest
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

    def test__play_round__calls_game_thread_once_when_two_players_in_lobby(self):
        player_1 = Player(uuid4(), "player 1", "update_url1")
        player_2 = Player(uuid4(), "player 2", "update_url2")
        lobby = {player_1.key: player_1,
                 player_2.key: player_2}

        tournament = Tournament(uuid4(), "Test Tournament", lobby)

        round = Round(1, 3, 3, 3)

        mock_scheduler = MagicMock(autospec=True)
        tournament.play_round(mock_scheduler, round)

        self.assertEqual(1, mock_scheduler.add_listener.call_count)
        self.assertEqual(1, mock_scheduler.add_job.call_count)
        self.assertEqual(1, len(tournament.rounds[0].games))
        self.assertEqual(1, len(tournament.games_in_progress))

    def test__play_round__calls_game_thread_thrice_when_three_players_in_lobby(self):
        player_1 = Player(uuid4(), "player 1", "update_url1")
        player_2 = Player(uuid4(), "player 2", "update_url2")
        player_3 = Player(uuid4(), "player 3", "update_url3")
        lobby = {player_1.key: player_1,
                 player_2.key: player_2,
                 player_3.key: player_3}

        tournament = Tournament(uuid4(), "Test Tournament", lobby)

        round = Round(1, 3, 3, 3)

        mock_scheduler = MagicMock(autospec=True)
        tournament.play_round(mock_scheduler, round)

        self.assertEqual(1, mock_scheduler.add_listener.call_count)
        self.assertEqual(3, mock_scheduler.add_job.call_count)
        self.assertEqual(3, len(tournament.rounds[0].games))
        self.assertEqual(3, len(tournament.games_in_progress))

    def test__play_round__throws_exception_when_round_is_already_in_progress(self):
        pass

    def test__process_completed_game__removes_a_key_from_games_in_progress(self):
        game = Game("Test Game", uuid4(), self.player_1, self.player_2)
        tournament = Tournament(uuid4(), "Test Tournament", [])
        tournament.games_in_progress.append(game.key)
        self.assertEqual(1, len(tournament.games_in_progress))

        event = JobExecutionEvent(1234, 4567, 'jobstore', 'whenever', retval=game)
        tournament._process_completed_game(event)

        self.assertEqual(0, len(tournament.games_in_progress))
