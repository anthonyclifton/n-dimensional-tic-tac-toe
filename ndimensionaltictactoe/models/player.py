class Player(object):
    def __init__(self, key, name, update_url):
        self.key = key
        self.name = name
        self.update_url = update_url
        self.winner = False
