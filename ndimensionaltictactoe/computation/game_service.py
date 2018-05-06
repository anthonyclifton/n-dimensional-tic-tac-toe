import uuid

from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.game_identifiers import GameIdentifiers


class GameService:
    def __init__(self):
        self.games = {}

    def create_game(self,
                    grid_size_x=3,
                    grid_size_y=3,
                    dimensions=2):
        game_name = 'game'
        game_key = uuid.uuid4()
        player_x_key = uuid.uuid4()
        player_o_key = uuid.uuid4()

        self.games[game_key] = Game(game_name,
                                    game_key,
                                    player_x_key,
                                    player_o_key,
                                    size_x=grid_size_x,
                                    size_y=grid_size_y,
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


