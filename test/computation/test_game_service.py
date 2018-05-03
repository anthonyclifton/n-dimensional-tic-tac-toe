from random import randint
from uuid import UUID

import pytest

from ndimensionaltictactoe.computation.game_service import GameService
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.game_identifiers import GameIdentifiers
from ndimensionaltictactoe.models.mark import Mark


game_service = GameService()


def test__create_game__should_return_grid_identifiers():
    grid_identifiers = game_service.create_game()
    assert isinstance(grid_identifiers, GameIdentifiers)
    assert UUID(str(grid_identifiers.grid_key))
    assert UUID(str(grid_identifiers.x_user_key))
    assert UUID(str(grid_identifiers.o_user_key))


def test__create_game__should_add_an_default_grid_object():
    grid_identifiers = game_service.create_game()

    grid = game_service.get_game_by_key(grid_identifiers.grid_key)
    assert isinstance(grid, Game)
    assert grid.key == grid_identifiers.grid_key
    assert grid.size == 3
    assert grid.dimensions == 2


def test__create_game_should_add_an_arbitrary_sized_grid():
    random_grid_size = randint(0, 999)
    grid_identifiers = game_service.create_game(grid_size=random_grid_size)
    grid = game_service.get_game_by_key(grid_identifiers.grid_key)
    assert grid.size == random_grid_size


def test__delete_game__should_remove_grid_from_service():
    grid_identifiers = game_service.create_game()

    grid_before = game_service.get_game_by_key(grid_identifiers.grid_key)
    assert grid_before.key == grid_identifiers.grid_key

    game_service.delete_game(grid_identifiers.grid_key)

    with pytest.raises(KeyError):
        game_service.get_game_by_key(grid_identifiers.grid_key)


def test__set_cell__should_add_the_mark_to_the_cell():
    mark = Mark(X_MARK, (0, 0))
    grid_identifiers = game_service.create_game()

    game_service.mark_cell(grid_identifiers.grid_key, mark)

    grid = game_service.get_game_by_key(grid_identifiers.grid_key)

    assert grid.cells[0] == mark


def test__set_cell__should_raise_exception_if_cell_already_marked():
    existing_mark = Mark(X_MARK, (0, 0))
    new_mark = Mark(O_MARK, (0, 0))

    grid_identifiers = game_service.create_game()

    game_service.mark_cell(grid_identifiers.grid_key, existing_mark)

    with pytest.raises(CellInUseException):
        game_service.mark_cell(grid_identifiers.grid_key, new_mark)
