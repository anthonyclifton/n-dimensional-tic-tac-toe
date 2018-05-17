import atexit
import logging
import uuid

from apscheduler.schedulers.background import BackgroundScheduler

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.models.round import Round
from ndimensionaltictactoe.models.tournament import Tournament
from ndimensionaltictactoe.schema.game_schema import PlayerXGameSchema, GameSummarySchema, PlayerOGameSchema, \
    PlayerSchema, LobbySchema, TournamentSchema

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

logging.basicConfig()


class GameService:
    def __init__(self):
        self.games = {}
        self.lobby = {}
        self.tournaments = {}

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

    def enter_lobby(self, player_name, update_url):
        player = Player(uuid.uuid4(), player_name, update_url)
        self.lobby[player.key] = player
        dumped_player, errors = PlayerSchema().dump(player)
        return dumped_player

    def get_lobby(self):
        dumped_players, errors = LobbySchema().dump({'lobby': self.lobby.values()})
        return dumped_players

    def create_tournament(self, tournament_name):
        new_tournament = Tournament(uuid.uuid4(),
                                    tournament_name,
                                    self.lobby)

        # TODO: deepcopy the lobby when starting the tournament so new players
        # in lobby don't end up messing up the scoreboard

        self.tournaments[new_tournament.key] = new_tournament

        dumped_tournaments, errors = TournamentSchema().dump(new_tournament)
        return dumped_tournaments

    def play_round(self, scheduler,
                   tournament_key,
                   x_size,
                   y_size,
                   winning_length):
        new_round = Round(x_size, y_size, winning_length)

        self.tournaments[tournament_key].play_round(scheduler, new_round)

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
