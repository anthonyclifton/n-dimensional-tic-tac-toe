import uuid

from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.game_identifiers import GameIdentifiers


class GameService:
    def __init__(self):
        self.games = {}

    def create_game(self, grid_size=3, dimensions=2):
        game_key = uuid.uuid4()
        player_x_key = uuid.uuid4()
        player_o_key = uuid.uuid4()

        self.games[game_key] = Game(game_key,
                                    player_x_key,
                                    player_o_key,
                                    size=grid_size,
                                    dimensions=dimensions)

        return GameIdentifiers(game_key,
                               player_x_key,
                               player_o_key)

    def get_game_by_key(self, key):
        return self.games[key]

    def delete_game(self, key):
        del self.games[key]

    def mark_cell(self, key, mark):
        game = self.get_game_by_key(key)
        game.mark_cell_by_coordinates(mark.coordinates, mark.value)


