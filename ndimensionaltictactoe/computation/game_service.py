import uuid

from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.schema.game_schema import PlayerXGameSchema, GameSummarySchema


class GameService:
    def __init__(self):
        self.games = {}

    def create_game(self,
                    name='no-name-game',
                    grid_size_x=3,
                    grid_size_y=3,
                    dimensions=2):

        game_key = uuid.uuid4()
        player_x = Player(uuid.uuid4(), 'player_x')
        player_o = None

        new_game = Game(name,
                        game_key,
                        player_x,
                        player_o,
                        size_x=grid_size_x,
                        size_y=grid_size_y,
                        dimensions=dimensions)

        self.games[game_key] = new_game

        dumped_game, errors = PlayerXGameSchema().dump(new_game)

        return dumped_game

    def get_game_by_key(self, key):
        return self.games[key]

    def get_games(self):
        return GameSummarySchema().dump(self.games.values(), many=True)

    def delete_game(self, key):
        del self.games[key]

    def mark_cell(self, key, mark):
        game = self.get_game_by_key(key)
        game.mark_cell_by_coordinates(mark.coordinates, mark.value)
