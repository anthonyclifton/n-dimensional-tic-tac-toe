import unittest
import uuid

import pytest

from ndimensionaltictactoe.exceptions.out_of_bounds_exception import OutOfBoundsException
from ndimensionaltictactoe.exceptions.winning_length_too_long_exception import WinningLengthTooLongException
from ndimensionaltictactoe.exceptions.winning_length_too_short import WinningLengthTooShortException
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.mark import Mark

PLAYER_X_KEY = uuid.uuid4()
PLAYER_O_KEY = uuid.uuid4()


class TestGame(unittest.TestCase):
    def test__init__should_raise_exception_when_dimensions_less_than_two(self):
        with pytest.raises(GridTooSmallException):
            Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 3, 1)

    def test__init__should_raise_exception_when_dimensions_greater_than_two(self):
        with pytest.raises(GridTooLargeException):
            Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 3, 3)

    def test__init__should_raise_exception_when_winning_length_too_short(self):
        with pytest.raises(WinningLengthTooShortException):
            Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 3, 2, 0)

    def test__init__should_raise_exception_when_winning_length_greater_than_shortest_side(self):
        with pytest.raises(WinningLengthTooLongException):
            Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 4, 2, 4)

    def test__get_cell_by_coordinates__returns_mark_at_coordinates(self):
        existing_mark_1 = Mark((0, 0), X_MARK)
        existing_mark_2 = Mark((1, 1), O_MARK)
        game = Game('test-game', PLAYER_X_KEY, PLAYER_O_KEY)
        game.cells.append(existing_mark_1)
        game.cells.append(existing_mark_2)

        actual_mark = game.get_cell_by_coordinates((1, 1))

        assert actual_mark == existing_mark_2

    def test__get_cell_by_coordinates__returns_none_if_coordinates_are_empty(self):
        existing_mark_1 = Mark((0, 0), X_MARK)
        game = Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY)
        game.cells.append(existing_mark_1)

        actual_mark = game.get_cell_by_coordinates((1, 1))

        assert not actual_mark

    def test__mark_cell_by_coordinates__adds_mark_to_cells(self):
        game = Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY)
        game.mark_cell_by_coordinates((1, 1), X_MARK)

        actual_mark = game.get_cell_by_coordinates((1, 1))

        assert actual_mark.value == X_MARK

    def test__mark_cell_by_coordinates_raises_exception_when_mark_outside(self):
        game = Game('test-grid',
                    PLAYER_X_KEY,
                    PLAYER_O_KEY)
        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates((-1, 0), X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates((0, -1), X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates((3, 0), X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates((0, 3), X_MARK)

    def test__mark_causes_win__should_return_true_if_horizontal_win(self):
        game = Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY)
        game.cells = [
            Mark((0, 0), X_MARK),
            Mark((2, 0), X_MARK)
        ]

        win = game.mark_causes_win(Mark((1, 0), X_MARK))

        assert win
