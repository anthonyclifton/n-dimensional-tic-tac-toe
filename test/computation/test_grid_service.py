from uuid import UUID

from ndimensionaltictactoe.computation.grid_service import GridService
from ndimensionaltictactoe.models.grid import Grid


def test__create_grid__should_return_a_guid_grid_key():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    UUID(str(grid_key))


def test__create_grid__should_add_an_default_grid_object():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    grid = grid_service.grids[grid_key]
    assert isinstance(grid, Grid)
    assert grid.size == 3
    assert grid.dimensions == 2
