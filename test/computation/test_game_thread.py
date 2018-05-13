import unittest
from uuid import uuid4

from mock import patch

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS, GAME_COMPLETED
from ndimensionaltictactoe.models.mark import X_MARK, Mark, O_MARK
from ndimensionaltictactoe.models.player import Player


class TestGameThread(unittest.TestCase):
    def setUp(self):
        self.player_x = Player(uuid4(),
                               "player x",
                               "http://testx/update")

        self.player_o = Player(uuid4(),
                               "player o",
                               "http://testo/update")
        self.game_key = uuid4()

        self.game = Game("Test Game",
                         self.game_key,
                         self.player_x,
                         self.player_o)

        self.game.state = GAME_INPROGRESS

    @patch('ndimensionaltictactoe.computation.game_thread._generic_post', autospec=True)
    def test__game_thread__will_terminate_in_size_x_times_size_y_moves_at_most(self,
                                                                               mock_post):
        mock_post.side_effect = _post_fake_no_winner
        game_thread(self.game)

        call_count = mock_post.call_count
        self.assertEqual(self.game.max_moves + 2, call_count)
        self.assertEqual(GAME_COMPLETED, self.game.state)
        self.assertEqual(False, self.game.player_x.winner)
        self.assertEqual(False, self.game.player_o.winner)

    @patch('ndimensionaltictactoe.computation.game_thread._generic_post', autospec=True)
    def test__game_thread__will_terminate_when_player_x_wins(self,
                                                             mock_post):
        mock_post.side_effect = _post_fake_x_wins
        game_thread(self.game)

        call_count = mock_post.call_count
        self.assertEqual(7, call_count)
        self.assertEqual(GAME_COMPLETED, self.game.state)
        self.assertEqual(True, self.game.player_x.winner)
        self.assertEqual(False, self.game.player_o.winner)

    @patch('ndimensionaltictactoe.computation.game_thread._generic_post', autospec=True)
    def test__game_thread__will_terminate_when_player_o_wins(self,
                                                             mock_post):
        mock_post.side_effect = _post_fake_o_wins
        game_thread(self.game)

        call_count = mock_post.call_count
        self.assertEqual(8, call_count)
        self.assertEqual(GAME_COMPLETED, self.game.state)
        self.assertEqual(False, self.game.player_x.winner)
        self.assertEqual(True, self.game.player_o.winner)


def _post_fake_no_winner(url, game):
    moves = [
        Mark(0, 0, X_MARK),
        Mark(1, 0, O_MARK),
        Mark(2, 0, X_MARK),
        Mark(1, 1, O_MARK),
        Mark(0, 1, X_MARK),
        Mark(2, 1, O_MARK),
        Mark(1, 2, X_MARK),
        Mark(0, 2, O_MARK),
        Mark(2, 2, X_MARK)
    ]

    if game.state == GAME_COMPLETED:
        return {'x': -1, 'y': -1}

    next_move = moves[len(game.cells)]
    return {'x': next_move.x, 'y': next_move.y}


def _post_fake_x_wins(url, game):
    moves = [
        Mark(0, 0, X_MARK),
        Mark(0, 1, O_MARK),
        Mark(1, 0, X_MARK),
        Mark(1, 1, O_MARK),
        Mark(2, 0, X_MARK)
    ]

    if game.state == GAME_COMPLETED:
        return {'x': -1, 'y': -1}

    next_move = moves[len(game.cells)]
    return {'x': next_move.x, 'y': next_move.y}


def _post_fake_o_wins(url, game):
    moves = [
        Mark(0, 0, X_MARK),
        Mark(0, 1, O_MARK),
        Mark(1, 0, X_MARK),
        Mark(1, 1, O_MARK),
        Mark(2, 2, X_MARK),
        Mark(2, 1, O_MARK)
    ]

    if game.state == GAME_COMPLETED:
        return {'x': -1, 'y': -1}

    next_move = moves[len(game.cells)]
    return {'x': next_move.x, 'y': next_move.y}
