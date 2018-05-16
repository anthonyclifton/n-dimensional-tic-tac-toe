class Round(object):
    def __init__(self, winner_points, x_size, y_size, winning_length):
        self.winner_points = winner_points
        self.x_size = x_size
        self.y_size = y_size
        self.winning_length = winning_length

        self.games_in_progress = []
        self.games = []
        self.winners = []
