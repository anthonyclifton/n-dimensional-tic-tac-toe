import itertools
from copy import deepcopy
from uuid import uuid4

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from ndimensionaltictactoe.computation.game_renderer import render_game_outcome, render_round_outcome
from ndimensionaltictactoe.computation.game_thread import game_thread
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK


class Tournament(object):
    def __init__(self, key, name, lobby):
        self.key = key
        self.name = name
        self.lobby = lobby

        self.rounds = []
        self.games_in_progress = []
        self.current_round = None

    def play_round(self, scheduler, round):
        self.rounds.append(round)
        self.current_round = round

        pairings = itertools.combinations(self.lobby.values(), 2)

        scheduler.add_listener(self._process_completed_game, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        for pairing in pairings:
            player_1 = pairing[0]
            player_2 = pairing[1]

            # TODO: since X always has the advantage, would it be better
            # to generate two games for each pairing?  To give them an
            # equal chance at the advantage?

            new_game = Game("{} vs {}".format(player_1.name, player_2.name),
                            uuid4(),
                            deepcopy(player_1),
                            deepcopy(player_2),
                            size_x=round.x_size,
                            size_y=round.y_size)
            new_game.state = GAME_INPROGRESS

            round.games.append(new_game)
            self.games_in_progress.append(new_game.key)
            self._start_game(scheduler, new_game)

    def get_scoreboard(self):
        scoreboards = [round.scoreboard for round in self.rounds]
        tournament_scoreboard = {}

        for scoreboard in scoreboards:
            for score in scoreboard:
                if score in tournament_scoreboard:
                    previous_score = tournament_scoreboard[score]
                    tournament_scoreboard[score] = previous_score + scoreboard[score]
                else:
                    tournament_scoreboard[score] = scoreboard[score]
        return tournament_scoreboard

    def _process_completed_game(self, event):
        game_key = event.retval.key
        self.games_in_progress.remove(game_key)

        if not self.games_in_progress:
            for game in self.current_round.games:
                render_game_outcome(game)
            self._score_games_in_round()
            render_round_outcome(self.name, self.current_round, len(self.rounds), self.lobby)

    def _score_games_in_round(self):
        # points are in increments of 2 so they can be split
        # a win gets you all the points
        # a loss gets you no points
        # a draw splits the points between the two players
        scoreboard = {}
        for game in self.current_round.games:
            if game.is_a_draw():
                self._assign_points(scoreboard, game.player_x, self.current_round.winner_points/2)
                self._assign_points(scoreboard, game.player_o, self.current_round.winner_points/2)
            elif game.player_x.winner:
                self._assign_points(scoreboard, game.player_x, self.current_round.winner_points)
                self._assign_points(scoreboard, game.player_o, 0)
            else:
                self._assign_points(scoreboard, game.player_x, 0)
                self._assign_points(scoreboard, game.player_o, self.current_round.winner_points)
        self.current_round.scoreboard = scoreboard

    def _assign_points(self, scoreboard, player, points):
        if player.key in scoreboard:
            previous_score = scoreboard[player.key]
            scoreboard[player.key] = previous_score + points
        else:
            scoreboard[player.key] = points

    def _start_game(self, scheduler, game):
        scheduler.add_job(
            func=game_thread,
            args=[game],
            id='game',
            name='Running game',
            replace_existing=True,
            max_instances=100)
