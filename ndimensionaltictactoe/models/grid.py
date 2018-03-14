from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException


class Grid(object):
    def __init__(self,
                 key,
                 player_x_key,
                 player_o_key,
                 size=3,
                 dimensions=2):
        if dimensions < 2:
            raise GridTooSmallException
        if dimensions > 3:
            raise GridTooLargeException
        self.key = key
        self.size = size
        self.dimensions = dimensions
        self.player_x_key = player_x_key
        self.player_o_key = player_o_key
        self.marks = []

    def get_mark_at_coordinates(self, coordinates):
        matches = [mark for mark in self.marks if mark.coordinates == coordinates]
        return matches[0] if len(matches) > 0 else None
