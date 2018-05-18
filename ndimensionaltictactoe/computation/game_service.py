import uuid
from copy import deepcopy

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS
from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.models.round import Round
from ndimensionaltictactoe.models.tournament import Tournament
from ndimensionaltictactoe.schema.game_schema import GameSummarySchema, \
    PlayerSchema, LobbySchema, TournamentSchema, GameSchema


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

        dumped_game, errors = GameSchema().dump(new_game)

        return dumped_game

    def join_game(self,
                  scheduler,
                  key,
                  player_name,
                  update_url):
        game = self.get_game_by_key(key)

        if game.state == GAME_INPROGRESS:
            raise GameInprogressException

        game.player_o = Player(uuid.uuid4(), player_name, update_url)
        game.state = GAME_INPROGRESS

        dumped_game, errors = GameSchema().dump(game)

        self._start_game(scheduler, game)

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
                                    deepcopy(self.lobby))

        self.tournaments[new_tournament.key] = new_tournament

        dumped_tournament, errors = TournamentSchema().dump(new_tournament)
        return dumped_tournament

    def close_tournaments(self):
        for tournament in self.tournaments.values():
            tournament.tournament_open = False

        dumped_tournaments, errors = TournamentSchema().dump(self.tournaments.values(), many=True)
        return dumped_tournaments

    def get_tournaments(self):
        dumped_tournaments, errors = TournamentSchema().dump(self.tournaments.values(), many=True)
        return dumped_tournaments

    def play_round(self, tournament_key, x_size, y_size, winning_length):
        tournament = self.tournaments[tournament_key]

        if tournament.tournament_open:
            new_round = Round(x_size, y_size, winning_length)
            tournament.play_round(new_round)
            return True

        return False

    def get_game_by_key(self, key):
        return self.games[key]

    def get_games(self):
        games, errors = GameSummarySchema().dump(self.games.values(), many=True)
        return games

    def delete_game(self, key):
        del self.games[key]

    @staticmethod
    def _start_game(scheduler, game):
        scheduler.add_job(
            func=game_thread,
            args=[game, True],
            id='game',
            name='Running game',
            replace_existing=True,
            max_instances=100)

