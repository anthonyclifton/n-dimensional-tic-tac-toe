import uuid

from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.exceptions.game_not_yet_inprogress_exception import GameNotYetInprogressException
from ndimensionaltictactoe.exceptions.not_valid_player_exception import NotValidPlayerException
from ndimensionaltictactoe.exceptions.not_your_turn_exception import NotYourTurnException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.schema.game_schema import PlayerXGameSchema, GameSummarySchema, PlayerOGameSchema


class GameService:
    def __init__(self):
        self.games = {}

    def create_game(self,
                    game_name,
                    grid_size_x=3,
                    grid_size_y=3,
                    dimensions=2):

        game_key = uuid.uuid4()
        player_x = Player(uuid.uuid4(), 'player_x', 'no-update-url')
        player_o = None

        new_game = Game(game_name,
                        game_key,
                        player_x,
                        player_o,
                        size_x=grid_size_x,
                        size_y=grid_size_y,
                        dimensions=dimensions)

        self.games[game_key] = new_game

        dumped_game, errors = PlayerXGameSchema().dump(new_game)

        return dumped_game

    def join_game(self, key, player_name):
        game = self.get_game_by_key(key)

        if game.state == GAME_INPROGRESS:
            raise GameInprogressException

        game.player_o = Player(uuid.uuid4(), player_name, 'no-update-url')
        game.state = GAME_INPROGRESS

        dumped_game, errors = PlayerOGameSchema().dump(game)

        return dumped_game

    def get_game_by_key(self, key):
        return self.games[key]

    def get_games(self):
        return GameSummarySchema().dump(self.games.values(), many=True)

    def delete_game(self, key):
        del self.games[key]

    def mark_cell(self, game_key, player_key, x, y):
        game = self.get_game_by_key(game_key)

        if game.state is not GAME_INPROGRESS:
            raise GameNotYetInprogressException

        if game.player_x.key == player_key:
            if not game.player_x_turn:
                raise NotYourTurnException
            game.mark_cell_by_coordinates(x, y, X_MARK)
            game.player_x_turn = False
            return PlayerXGameSchema().dump(game)
        elif game.player_o and (game.player_o.key == player_key):
            if game.player_x_turn:
                raise NotYourTurnException
            game.mark_cell_by_coordinates(x, y, O_MARK)
            game.player_x_turn = True
            return PlayerOGameSchema().dump(game)
        else:
            raise NotValidPlayerException
