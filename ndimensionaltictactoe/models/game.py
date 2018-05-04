from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.models.mark import Mark


class Game(object):
    def __init__(self,
                 key,
                 player_x_key,
                 player_o_key,
                 size_x=3,
                 size_y=3,
                 dimensions=2):
        if dimensions < 2:
            raise GridTooSmallException
        if dimensions > 2:
            raise GridTooLargeException
        self.key = key
        self.size_x = size_x
        self.size_y = size_y
        self.dimensions = dimensions
        self.player_x_key = player_x_key
        self.player_o_key = player_o_key
        self.cells = []

    def get_cell_by_coordinates(self, coordinates):
        return next((mark for mark in self.cells if mark.coordinates == coordinates), None)

    def mark_cell_by_coordinates(self, coordinates, mark):
        if not self.get_cell_by_coordinates(coordinates):
            self.cells.append(Mark(coordinates, mark))
        else:
            raise CellInUseException
