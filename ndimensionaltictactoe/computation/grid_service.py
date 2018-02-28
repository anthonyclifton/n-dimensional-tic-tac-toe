import uuid


class GridService:
    def __init__(self):
        self.grids = {}

    def create_grid(self, grid_size=3):
        grid_key = uuid.uuid4()

        new_grid = [[None for col in range(grid_size)] for row in range(grid_size)]

        self.grids[grid_key] = new_grid

        return grid_key
