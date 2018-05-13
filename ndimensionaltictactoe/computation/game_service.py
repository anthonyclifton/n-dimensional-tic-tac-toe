import atexit
import logging
import uuid

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.schema.game_schema import PlayerXGameSchema, GameSummarySchema, PlayerOGameSchema

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

logging.basicConfig()


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
        self._start_game(game)
        return dumped_game

    def get_game_by_key(self, key):
        return self.games[key]

    def get_games(self):
        games, errors = GameSummarySchema().dump(self.games.values(), many=True)
        return games

    def delete_game(self, key):
        del self.games[key]

    @staticmethod
    def _start_game(game):
        print("Starting game: {}".format(game.name))
        scheduler.add_job(
            func=game_thread,
            args=[game],
            id='game',
            name='Running game',
            replace_existing=True,
            max_instances=100)



