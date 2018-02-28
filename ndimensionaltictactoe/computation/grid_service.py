import uuid


class GridService:
    def __init__(self):
        self.grids = {}

    def create_grid(self):
        return uuid.uuid4()
