class Round(object):
    def __init__(self, x_size, y_size, winning_length):
        self.winner_points = int(max([x_size, y_size]) / 3) * 2
        self.x_size = x_size
        self.y_size = y_size
        self.winning_length = winning_length

        self.games = []
        self.scoreboard = None
