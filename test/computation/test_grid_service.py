from uuid import UUID

from ndimensionaltictactoe.computation.grid_service import GridService


def test__create_grid__should_return_a_guid_grid_key():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    UUID(str(grid_key))


def test__create_grid__should_add_new_grid_to_grids_map():
    grid_service = GridService()

    assert len(grid_service.grids) == 0

    grid_key = grid_service.create_grid()

    assert len(grid_service.grids) == 1
    assert grid_service.grids[grid_key] == []
