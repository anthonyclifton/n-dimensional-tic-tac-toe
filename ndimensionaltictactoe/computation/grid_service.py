import uuid


class GridService:
    def __init__(self):
        self.grids = {}

    def create_grid(self):
        grid_key = uuid.uuid4()
        self.grids[grid_key] = []
        return grid_key
