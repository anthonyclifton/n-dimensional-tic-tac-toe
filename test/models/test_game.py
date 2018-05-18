import unittest
import uuid

import pytest

from ndimensionaltictactoe.exceptions.no_name_exception import NoNameException
from ndimensionaltictactoe.exceptions.out_of_bounds_exception import OutOfBoundsException
from ndimensionaltictactoe.exceptions.winning_length_too_long_exception import WinningLengthTooLongException
from ndimensionaltictactoe.exceptions.winning_length_too_short import WinningLengthTooShortException
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.models.game import Game, GAME_CREATED_WAITING
from ndimensionaltictactoe.models.mark import Mark
from ndimensionaltictactoe.models.player import Player

PLAYER_X = Player(uuid.uuid4(), 'player_x', 'http://localhost/update')
PLAYER_O = Player(uuid.uuid4(), 'player_o', 'http://localhost/update')


class TestGame(unittest.TestCase):
    def test__init__should_raise_exception_when_dimensions_less_than_two(self):
        with pytest.raises(GridTooSmallException):
            Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O, 3, 3, 3, 1)

    def test__init__should_raise_exception_when_dimensions_greater_than_two(self):
        with pytest.raises(GridTooLargeException):
            Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O, 3, 3, 3, 3)

    def test__init__should_raise_exception_when_winning_length_too_short(self):
        with pytest.raises(WinningLengthTooShortException):
            Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O, 3, 3, 0, 2)

    def test__init__should_raise_exception_when_winning_length_greater_than_shortest_side(self):
        with pytest.raises(WinningLengthTooLongException):
            Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O, 3, 4, 4, 2)

    def test__init__should_raise_exception_when_name_is_empty(self):
        with pytest.raises(NoNameException):
            Game('', uuid.uuid4(), PLAYER_X, PLAYER_O)

        with pytest.raises(NoNameException):
            Game(None, uuid.uuid4(), PLAYER_X, PLAYER_O)

    def test__init__should_start_in_created_waiting_state(self):
        game = Game('test-game', uuid.uuid4(), PLAYER_X, PLAYER_O)
        assert game.state == GAME_CREATED_WAITING

    def test__get_cell_by_coordinates__returns_mark_at_coordinates(self):
        existing_mark_1 = Mark(0, 0, X_MARK)
        existing_mark_2 = Mark(1, 1, O_MARK)
        game = Game('test-game', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells.append(existing_mark_1)
        game.cells.append(existing_mark_2)

        actual_mark = game.get_cell_by_coordinates(1, 1)

        assert actual_mark == existing_mark_2

    def test__get_cell_by_coordinates__returns_none_if_coordinates_are_empty(self):
        existing_mark_1 = Mark(0, 0, X_MARK)
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells.append(existing_mark_1)

        actual_mark = game.get_cell_by_coordinates(1, 1)

        assert not actual_mark

    def test__mark_cell_by_coordinates__adds_mark_to_cells(self):
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.mark_cell_by_coordinates(1, 1, X_MARK)

        actual_mark = game.get_cell_by_coordinates(1, 1)

        assert actual_mark.value == X_MARK

    def test__mark_cell_by_coordinates_raises_exception_when_mark_outside(self):
        game = Game('test-grid',
                    uuid.uuid4(),
                    PLAYER_X,
                    PLAYER_O)
        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates(-1, 0, X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates(0, -1, X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates(3, 0, X_MARK)

        with pytest.raises(OutOfBoundsException):
            game.mark_cell_by_coordinates(0, 3, X_MARK)

    def test__mark_causes_win__should_return_true_if_horizontal_win(self):
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells = [
            Mark(0, 0, X_MARK),
            Mark(2, 0, X_MARK)
        ]

        win = game.mark_causes_win(Mark(1, 0, X_MARK))

        assert win

    def test__mark_causes_win__should_return_true_if_vertical_win(self):
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells = [
            Mark(0, 0, X_MARK),
            Mark(0, 2, X_MARK)
        ]

        win = game.mark_causes_win(Mark(0, 1, X_MARK))

        assert win

    def test__mark_causes_win__should_return_true_if_negative_slope_diagonal_win(self):
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells = [
            Mark(0, 0, X_MARK),
            Mark(2, 2, X_MARK)
        ]

        win = game.mark_causes_win(Mark(1, 1, X_MARK))

        assert win

    def test__mark_causes_win__should_return_true_if_positive_slope_diagonal_win(self):
        game = Game('test-grid', uuid.uuid4(), PLAYER_X, PLAYER_O)
        game.cells = [
            Mark(0, 2, X_MARK),
            Mark(2, 0, X_MARK)
        ]

        win = game.mark_causes_win(Mark(1, 1, X_MARK))

        assert win
