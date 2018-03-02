import uuid

import numpy as np

from ndimensionaltictactoe.models.grid import Grid
from ndimensionaltictactoe.models.mark import Mark


class GridService:
    def __init__(self):
        self.grids = {}

    def create_grid(self, grid_size=3, dimensions=2):
        grid_key = uuid.uuid4()

        # grid_shape = tuple([grid_size for dimension in range(dimensions)])
        # new_grid = np.zeros(grid_shape, dtype=int)

        self.grids[grid_key] = Grid(grid_key)

        return grid_key

    def get_grid_by_key(self, key):
        return self.grids[key]

    def delete_grid(self, key):
        del self.grids[key]

    def add_mark(self, key, mark):
        grid = self.get_grid_by_key(key)
        grid.marks.append(mark)

