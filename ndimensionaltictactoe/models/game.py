from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException


class Game(object):
    def __init__(self,
                 key,
                 player_x_key,
                 player_o_key,
                 size=3,
                 dimensions=2):
        if dimensions < 2:
            raise GridTooSmallException
        if dimensions > 2:
            raise GridTooLargeException
        self.key = key
        self.size = size
        self.dimensions = dimensions
        self.player_x_key = player_x_key
        self.player_o_key = player_o_key
        self.cells = []

    def get_cell_by_coordinates(self, coordinates):
        return next((mark for mark in self.cells if mark.coordinates == coordinates), None)
