import unittest
from random import randint
from uuid import UUID, uuid4

import pytest

from ndimensionaltictactoe.computation.game_service import GameService
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.exceptions.game_not_yet_inprogress_exception import GameNotYetInprogressException
from ndimensionaltictactoe.exceptions.not_valid_player_exception import NotValidPlayerException
from ndimensionaltictactoe.exceptions.not_your_turn_exception import NotYourTurnException
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS


class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_name = 'Test Game'
        self.game_service = GameService()
        self.game = self.game_service.create_game(self.game_name)
        self.game_key = UUID(self.game['key'])
        self.player_x_key = UUID(self.game['player_x']['key'])

    def test__create_game__should_return_a_dictionary(self):
        self.assertEqual(self.game['name'], self.game_name)
        self.assertEqual(self.game['size_x'], 3)
        self.assertEqual(self.game['size_y'], 3)
        self.assertEqual(self.game['player_x']['name'], 'player_x')
        self.assertEqual(self.game['cells'], [])
        self.assertEqual(self.game['winning_length'], 3)

    def test__create_game__should_add_a_default_game_object(self):
        game = self.game_service.get_game_by_key(UUID(self.game['key']))

        assert isinstance(game, Game)
        assert game.key == self.game_key
        assert game.size_x == 3
        assert game.size_y == 3
        assert game.dimensions == 2
        assert game.player_x_turn

    def test__create_game_should_add_an_arbitrary_sized_game(self):
        random_game_size_x = randint(0, 999)
        random_game_size_y = randint(0, 999)
        custom_sized_game = self.game_service.create_game(
            'Test Game',
            grid_size_x=random_game_size_x,
            grid_size_y=random_game_size_y)
        game = self.game_service.get_game_by_key(UUID(custom_sized_game['key']))
        assert game.size_x == random_game_size_x
        assert game.size_y == random_game_size_y

    def test__join_game__should_add_player_o_to_game(self):
        joined_game = self.game_service.join_game(self.game_key, 'test name')

        updated_game = self.game_service.get_game_by_key(self.game_key)

        assert updated_game.player_o
        assert UUID(str(updated_game.player_o.key))
        assert updated_game.player_o.name == 'test name'
        assert updated_game.state == GAME_INPROGRESS

        self.assertEqual(joined_game['name'], self.game_name)
        assert UUID(joined_game['key'])
        self.assertEqual(joined_game['size_x'], 3)
        self.assertEqual(joined_game['size_y'], 3)
        assert UUID(joined_game['player_o']['key'])
        self.assertEqual(joined_game['player_o']['name'], updated_game.player_o.name)
        self.assertEqual(joined_game['cells'], [])
        self.assertEqual(joined_game['winning_length'], 3)

    def test__join_game__should_raise_exception_when_game_already_in_progress(self):
        self.game_service.join_game(self.game_key, 'player who is on time')

        with pytest.raises(GameInprogressException):
            self.game_service.join_game(self.game_key, 'player who is too late')

    def test__delete_game__should_remove_game_from_service(self):
        assert self.game_service.get_game_by_key(self.game_key)

        self.game_service.delete_game(self.game_key)

        with pytest.raises(KeyError):
            self.game_service.get_game_by_key(self.game_key)

    def test__mark_cell__should_add_the_mark_to_the_cell(self):
        self.game_service.join_game(self.game_key, "second player")

        self.game_service.mark_cell(self.game_key, self.player_x_key, 0, 0)

        game = self.game_service.get_game_by_key(self.game_key)

        first_cell = game.cells[0]
        self.assertEqual(first_cell.x, 0)
        self.assertEqual(first_cell.y, 0)
        self.assertEqual(first_cell.value, X_MARK)

    def test__mark_cell_should_mark_x_when_player_x_is_marking_and_return_updated_game(self):
        dumped_game = self.game_service.create_game('Test Game')
        game_key = UUID(dumped_game['key'])
        player_key = UUID(dumped_game['player_x']['key'])

        self.game_service.join_game(game_key, "second player")

        updated_game, errors = self.game_service.mark_cell(game_key, player_key, 1, 1)

        self.assertEqual(updated_game['cells'][0]['value'], X_MARK)
        self.assertEqual(updated_game['cells'][0]['x'], 1)
        self.assertEqual(updated_game['cells'][0]['y'], 1)

    def test__mark_cell_should_mark_o_when_player_o_is_marking_and_return_updated_game(self):
        dumped_game = self.game_service.create_game('Test Game')
        game_key = UUID(dumped_game['key'])
        player_x_key = UUID(dumped_game['player_x']['key'])

        joined_game = self.game_service.join_game(game_key, 'player_o')
        player_o_key = UUID(joined_game['player_o']['key'])

        self.game_service.mark_cell(game_key, player_x_key, 0, 0)
        updated_game, errors = self.game_service.mark_cell(game_key, player_o_key, 1, 1)

        self.assertEqual(updated_game['cells'][1]['value'], O_MARK)
        self.assertEqual(updated_game['cells'][1]['x'], 1)
        self.assertEqual(updated_game['cells'][1]['y'], 1)

    def test__mark_cell__should_raise_exception_if_cell_already_marked(self):
        dumped_game = self.game_service.create_game('Test Game')
        game_key = UUID(dumped_game['key'])
        player_x_key = UUID(dumped_game['player_x']['key'])

        joined_game = self.game_service.join_game(game_key, 'player_o')
        player_o_key = UUID(joined_game['player_o']['key'])

        self.game_service.mark_cell(game_key, player_x_key, 0, 0)

        with pytest.raises(CellInUseException):
            self.game_service.mark_cell(game_key, player_o_key, 0, 0)

    def test__mark_cell__should_update_to_player_o_turn_when_player_x_marks(self):
        dumped_game = self.game_service.create_game('Test Game')
        game_key = UUID(dumped_game['key'])
        player_x_key = UUID(dumped_game['player_x']['key'])

        self.game_service.join_game(game_key, 'player_o')
        self.game_service.mark_cell(game_key, player_x_key, 0, 0)
        updated_game = self.game_service.get_game_by_key(game_key)

        assert not updated_game.player_x_turn

    def test__mark_cell__should_update_to_player_x_turn_when_player_o_marks(self):
        dumped_game = self.game_service.create_game('Test Game')
        game_key = UUID(dumped_game['key'])
        player_x_key = UUID(dumped_game['player_x']['key'])

        joined_game = self.game_service.join_game(game_key, 'player_o')
        player_o_key = UUID(joined_game['player_o']['key'])

        self.game_service.mark_cell(game_key, player_x_key, 0, 0)
        self.game_service.mark_cell(game_key, player_o_key, 0, 1)

        updated_game = self.game_service.get_game_by_key(game_key)

        assert updated_game.player_x_turn

    def test__mark_cell__should_raise_exception_when_third_player_marks(self):
        game = self.game_service.create_game('Test Game')
        game_key = UUID(game['key'])

        self.game_service.join_game(game_key, 'player_o')

        with pytest.raises(NotValidPlayerException):
            self.game_service.mark_cell(game_key, uuid4(), 0, 0)

    def test__mark_cell__should_raise_exception_if_not_o_players_turn_yet(self):
        game = self.game_service.create_game('Test Game')
        game_key = UUID(game['key'])

        joined_game = self.game_service.join_game(game_key, 'player_o')
        player_o_key = UUID(joined_game['player_o']['key'])

        with pytest.raises(NotYourTurnException):
            self.game_service.mark_cell(game_key, player_o_key, 0, 0)

    def test__mark_cell__should_raise_exception_if_not_x_players_turn_yet(self):
        game = self.game_service.create_game('Test Game')
        game_key = UUID(game['key'])
        player_x_key = UUID(game['player_x']['key'])

        self.game_service.join_game(game_key, 'player_o')

        self.game_service.mark_cell(game_key, player_x_key, 0, 0)

        with pytest.raises(NotYourTurnException):
            self.game_service.mark_cell(game_key, player_x_key, 1, 1)

    def test__mark_cell__should_raise_exception_if_game_not_yet_inprogress(self):
        game = self.game_service.create_game('Test Game')
        game_key = UUID(game['key'])
        player_x_key = UUID(game['player_x']['key'])

        with pytest.raises(GameNotYetInprogressException):
            self.game_service.mark_cell(game_key, player_x_key, 1, 1)

    def test__get_games__should_return_all_created_games_summary(self):
        self.game_service.create_game('Test Game')
        self.game_service.create_game('Test Game 2')

        games_list = self.game_service.get_games()
        self.assertEqual(len(games_list), 2)
