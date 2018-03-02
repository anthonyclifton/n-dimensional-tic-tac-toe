from uuid import UUID

import pytest

from ndimensionaltictactoe.computation.grid_service import GridService
from ndimensionaltictactoe.computation.mark_value import X
from ndimensionaltictactoe.models.grid import Grid
from ndimensionaltictactoe.models.mark import Mark


def test__create_grid__should_return_a_guid_grid_key():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    UUID(str(grid_key))


def test__create_grid__should_add_an_default_grid_object():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    grid = grid_service.get_grid_by_key(grid_key)
    assert isinstance(grid, Grid)
    assert grid.key == grid_key
    assert grid.size == 3
    assert grid.dimensions == 2


def test__delete_grid__should_remove_grid_from_service():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    grid_before = grid_service.get_grid_by_key(grid_key)
    assert grid_before.key == grid_key

    grid_service.delete_grid(grid_key)

    with pytest.raises(KeyError):
        grid_service.get_grid_by_key(grid_key)


def test__add_mark__should_add_the_mark_to_the_grid():
    mark = Mark(X, (0, 0))
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    grid_service.add_mark(grid_key, mark)

    grid = grid_service.get_grid_by_key(grid_key)

    assert grid.marks[0] == mark
