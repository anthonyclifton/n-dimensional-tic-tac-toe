class Tournament(object):
    def __init__(self, key, name, lobby):
        self.key = key
        self.name = name
        self.lobby = lobby

        self.rounds = []

    def play_round(self, round):
        self.rounds.append(round)
