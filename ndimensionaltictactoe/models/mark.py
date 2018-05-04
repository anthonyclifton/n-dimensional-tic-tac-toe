O_MARK = 1
X_MARK = 2


class Mark(object):
    def __init__(self, coordinates, value):
        self.coordinates = coordinates
        self.value = value
