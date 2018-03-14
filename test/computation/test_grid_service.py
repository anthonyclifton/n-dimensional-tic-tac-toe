from random import randint
from uuid import UUID

import pytest

from ndimensionaltictactoe.computation.grid_service import GridService
from ndimensionaltictactoe.computation.mark_value import X, O
from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.grid import Grid
from ndimensionaltictactoe.models.mark import Mark


grid_service = GridService()


def test__create_grid__should_return_a_guid_grid_key():
    grid_key = grid_service.create_grid()
    UUID(str(grid_key))


def test__create_grid__should_add_an_default_grid_object():
    grid_key = grid_service.create_grid()

    grid = grid_service.get_grid_by_key(grid_key)
    assert isinstance(grid, Grid)
    assert grid.key == grid_key
    assert grid.size == 3
    assert grid.dimensions == 2


def test__create_grid_should_add_a_three_dimensional_grid():
    grid_key = grid_service.create_grid(dimensions=3)
    grid = grid_service.get_grid_by_key(grid_key)
    assert grid.dimensions == 3


def test__create_grid_should_add_an_arbitrary_sized_grid():
    random_grid_size = randint(0, 999)
    grid_key = grid_service.create_grid(grid_size=random_grid_size)
    grid = grid_service.get_grid_by_key(grid_key)
    assert grid.size == random_grid_size


def test__delete_grid__should_remove_grid_from_service():
    grid_key = grid_service.create_grid()

    grid_before = grid_service.get_grid_by_key(grid_key)
    assert grid_before.key == grid_key

    grid_service.delete_grid(grid_key)

    with pytest.raises(KeyError):
        grid_service.get_grid_by_key(grid_key)


def test__add_mark__should_add_the_mark_to_the_grid():
    mark = Mark(X, (0, 0))
    grid_key = grid_service.create_grid()

    grid_service.add_mark(grid_key, mark)

    grid = grid_service.get_grid_by_key(grid_key)

    assert grid.marks[0] == mark


def test__add_mark__should_raise_exception_if_space_already_filled():
    existing_mark = Mark(X, (0, 0))
    new_mark = Mark(O, (0, 0))

    grid_key = grid_service.create_grid()

    grid_service.add_mark(grid_key, existing_mark)

    with pytest.raises(CellInUseException):
        grid_service.add_mark(grid_key, new_mark)
