from uuid import UUID

from ndimensionaltictactoe.computation.grid_service import GridService


def test__create_grid__should_return_a_guid_grid_key():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    UUID(str(grid_key))


def test__init__should_create_an_empty_grid_dictionary():
    grid_service = GridService()
    assert grid_service.grids == {}
