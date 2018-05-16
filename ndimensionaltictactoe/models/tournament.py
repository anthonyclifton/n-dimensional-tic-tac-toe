from uuid import uuid4

from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.models.game import Game


class Tournament(object):
    def __init__(self, key, name, lobby):
        self.key = key
        self.name = name
        self.lobby = lobby

        self.rounds = []

    def play_round(self, scheduler, round):
        self.rounds.append(round)

        player_1 = self.lobby.values()[0]
        player_2 = self.lobby.values()[1]

        new_game = Game("{} vs {}".format(player_1.name, player_2.name),
                        uuid4(),
                        player_1,
                        player_2,
                        size_x=round.x_size,
                        size_y=round.y_size)

        self._start_game(scheduler, new_game)

    @staticmethod
    def _start_game(scheduler, game):
        print("Starting game: {}".format(game.name))
        scheduler.add_job(
            func=game_thread,
            args=[game],
            id='game',
            name='Running game',
            replace_existing=True,
            max_instances=100)
