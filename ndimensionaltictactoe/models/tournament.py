import itertools
from uuid import uuid4

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.models.game import Game


class Tournament(object):
    def __init__(self, key, name, lobby):
        self.key = key
        self.name = name
        self.lobby = lobby

        self.rounds = []
        self.games_in_progress = []

    def play_round(self, scheduler, round):
        self.rounds.append(round)

        pairings = itertools.combinations(self.lobby.values(), 2)

        scheduler.add_listener(self._process_completed_game, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        for pairing in pairings:
            player_1 = pairing[0]
            player_2 = pairing[1]

            new_game = Game("{} vs {}".format(player_1.name, player_2.name),
                            uuid4(),
                            player_1,
                            player_2,
                            size_x=round.x_size,
                            size_y=round.y_size)

            round.games.append(new_game)
            self.games_in_progress.append(new_game.key)
            self._start_game(scheduler, new_game)

    def _process_completed_game(self, event):
        game_key = event.retval.key
        self.games_in_progress.remove(game_key)

    def _start_game(self, scheduler, game):
        print("Starting game: {}".format(game.name))
        scheduler.add_job(
            func=game_thread,
            args=[game],
            id='game',
            name='Running game',
            replace_existing=True,
            max_instances=100)
