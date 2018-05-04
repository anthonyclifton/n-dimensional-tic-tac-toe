import unittest
from random import randint
from uuid import UUID

import pytest

from ndimensionaltictactoe.computation.game_service import GameService
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.game_identifiers import GameIdentifiers
from ndimensionaltictactoe.models.mark import Mark


class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()

    def test__create_game__should_return_game_identifiers(self):
        game_identifiers = self.game_service.create_game()
        assert isinstance(game_identifiers, GameIdentifiers)
        assert UUID(str(game_identifiers.grid_key))
        assert UUID(str(game_identifiers.x_user_key))
        assert UUID(str(game_identifiers.o_user_key))

    def test__create_game__should_add_a_default_game_object(self):
        game_identifiers = self.game_service.create_game()

        game = self.game_service.get_game_by_key(game_identifiers.grid_key)
        assert isinstance(game, Game)
        assert game.key == game_identifiers.grid_key
        assert game.size_x == 3
        assert game.size_y == 3
        assert game.dimensions == 2

    def test__create_game_should_add_an_arbitrary_sized_game(self):
        random_game_size_x = randint(0, 999)
        random_game_size_y = randint(0, 999)
        game_identifiers = self.game_service.create_game(
            grid_size_x=random_game_size_x,
            grid_size_y=random_game_size_y)
        game = self.game_service.get_game_by_key(game_identifiers.grid_key)
        assert game.size_x == random_game_size_x
        assert game.size_y == random_game_size_y

    def test__delete_game__should_remove_game_from_service(self):
        game_identifiers = self.game_service.create_game()

        game_before = self.game_service.get_game_by_key(game_identifiers.grid_key)
        assert game_before.key == game_identifiers.grid_key

        self.game_service.delete_game(game_identifiers.grid_key)

        with pytest.raises(KeyError):
            self.game_service.get_game_by_key(game_identifiers.grid_key)

    def test__mark_cell__should_add_the_mark_to_the_cell(self):
        mark = Mark((0, 0), X_MARK)
        game_identifiers = self.game_service.create_game()

        self.game_service.mark_cell(game_identifiers.grid_key, mark)

        game = self.game_service.get_game_by_key(game_identifiers.grid_key)

        first_cell = game.cells[0]
        self.assertEqual(first_cell.coordinates, mark.coordinates)
        self.assertEqual(first_cell.value, mark.value)

    def test__mark_cell__should_raise_exception_if_cell_already_marked(self):
        existing_mark = Mark((0, 0), X_MARK)
        new_mark = Mark((0, 0), O_MARK)

        game_identifiers = self.game_service.create_game()

        self.game_service.mark_cell(game_identifiers.grid_key, existing_mark)

        with pytest.raises(CellInUseException):
            self.game_service.mark_cell(game_identifiers.grid_key, new_mark)
