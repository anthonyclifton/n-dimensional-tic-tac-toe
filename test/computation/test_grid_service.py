from uuid import UUID

from ndimensionaltictactoe.computation.grid_service import GridService


def test__create_grid__should_return_a_guid_grid_key():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    UUID(str(grid_key))


def test__create_grid__should_add_a_grid_of_default_size():
    grid_service = GridService()

    grid_key = grid_service.create_grid()

    grid = grid_service.grids[grid_key]
    assert len(grid) == 3
    for column in grid:
        assert len(column) == 3


def test__create_grid__should_add_grid_of_non_default_size():
    grid_service = GridService()

    grid_key = grid_service.create_grid(4)

    grid = grid_service.grids[grid_key]
    assert len(grid) == 4
    for column in grid:
        assert len(column) == 4


def test__create_grid__should_add_grid_of_3_dimensions():
    grid_service = GridService()

    grid_key = grid_service.create_grid(grid_size=2, dimensions=3)

    grid = grid_service.grids[grid_key]
    print grid.tolist()
    assert grid.tolist() == [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
