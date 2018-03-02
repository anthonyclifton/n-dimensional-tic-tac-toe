from ndimensionaltictactoe.computation.mark_value import X, O
from ndimensionaltictactoe.models.grid import Grid
from ndimensionaltictactoe.models.mark import Mark


def test__get_mark_at_coordinates__returns_mark_at_coordinates():
    existing_mark_1 = Mark(X, (0, 0))
    existing_mark_2 = Mark(O, (1, 1))
    grid = Grid('test-grid')
    grid.marks.append(existing_mark_1)
    grid.marks.append(existing_mark_2)

    actual_mark = grid.get_mark_at_coordinates((1, 1))

    assert actual_mark == existing_mark_2


def test__get_mark_at_coordinates__returns_none_if_coordinates_are_empty():
    existing_mark_1 = Mark(X, (0, 0))
    grid = Grid('test-grid')
    grid.marks.append(existing_mark_1)

    actual_mark = grid.get_mark_at_coordinates((1, 1))

    assert not actual_mark
