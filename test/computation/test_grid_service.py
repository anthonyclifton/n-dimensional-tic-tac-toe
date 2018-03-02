from uuid import UUID

import pytest

from ndimensionaltictactoe.computation.grid_service import GridService
from ndimensionaltictactoe.models.grid import Grid


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
