import uuid

from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.game_identifiers import GameIdentifiers


class GameService:
    def __init__(self):
        self.grids = {}

    def create_grid(self, grid_size=3, dimensions=2):
        grid_key = uuid.uuid4()
        player_x_key = uuid.uuid4()
        player_o_key = uuid.uuid4()

        self.grids[grid_key] = Game(grid_key,
                                    player_x_key,
                                    player_o_key,
                                    size=grid_size,
                                    dimensions=dimensions)

        return GameIdentifiers(grid_key,
                               player_x_key,
                               player_o_key)

    def get_grid_by_key(self, key):
        return self.grids[key]

    def delete_grid(self, key):
        del self.grids[key]

    def add_mark(self, key, mark):
        grid = self.get_grid_by_key(key)
        if not grid.get_mark_at_coordinates(mark.coordinates):
            grid.marks.append(mark)
        else:
            raise CellInUseException

