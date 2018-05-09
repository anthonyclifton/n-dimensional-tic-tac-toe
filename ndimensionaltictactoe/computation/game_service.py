import uuid

import requests

from ndimensionaltictactoe.exceptions.game_already_completed_exception import GameAlreadyCompletedException
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.exceptions.game_not_yet_inprogress_exception import GameNotYetInprogressException
from ndimensionaltictactoe.exceptions.not_valid_player_exception import NotValidPlayerException
from ndimensionaltictactoe.exceptions.not_your_turn_exception import NotYourTurnException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS, GAME_COMPLETED, GAME_CREATED_WAITING
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.schema.game_schema import PlayerXGameSchema, GameSummarySchema, PlayerOGameSchema


class GameService:
    def __init__(self):
        self.games = {}

    def create_game(self,
                    game_name,
                    player_name,
                    update_url,
                    grid_size_x=3,
                    grid_size_y=3,
                    dimensions=2):

        game_key = uuid.uuid4()
        player_x = Player(uuid.uuid4(), player_name, update_url)
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

    def join_game(self, key, player_name, update_url):
        game = self.get_game_by_key(key)

        if game.state == GAME_INPROGRESS:
            raise GameInprogressException

        game.player_o = Player(uuid.uuid4(), player_name, update_url)
        game.state = GAME_INPROGRESS

        dumped_game, errors = PlayerOGameSchema().dump(game)
        updated_game, errors = PlayerXGameSchema().dump(game)

        self.update_player(updated_game, game.player_x.update_url)

        return dumped_game

    def get_game_by_key(self, key):
        return self.games[key]

    def get_games(self):
        games, errors = GameSummarySchema().dump(self.games.values(), many=True)
        return games

    def delete_game(self, key):
        del self.games[key]

    def mark_cell(self, game_key, player_key, x, y):
        game = self.get_game_by_key(game_key)

        if game.state is GAME_CREATED_WAITING:
            raise GameNotYetInprogressException

        if game.state is GAME_COMPLETED:
            raise GameAlreadyCompletedException

        if game.player_x.key == player_key:
            if not game.player_x_turn:
                raise NotYourTurnException
            game.mark_cell_by_coordinates(x, y, X_MARK)
            game.player_x_turn = False
            dumped_game, errors = PlayerXGameSchema().dump(game)
            updated_game, errors = PlayerOGameSchema().dump(game)
            self.update_player(updated_game, game.player_o.update_url)
            return dumped_game
        elif game.player_o and (game.player_o.key == player_key):
            if game.player_x_turn:
                raise NotYourTurnException
            game.mark_cell_by_coordinates(x, y, O_MARK)
            game.player_x_turn = True
            dumped_game, errors = PlayerOGameSchema().dump(game)
            updated_game, errors = PlayerXGameSchema().dump(game)
            self.update_player(updated_game, game.player_x.update_url)
            return dumped_game
        else:
            raise NotValidPlayerException

    def update_player(self, dumped_game, update_url):
            payload = dumped_game
            self._generic_post(update_url, payload)

    @staticmethod
    def _generic_post(url, payload):
        return requests.post(url, json=payload)

