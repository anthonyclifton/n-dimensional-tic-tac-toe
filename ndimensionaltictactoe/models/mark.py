O_MARK = 1
X_MARK = 2


class Mark(object):
    def __init__(self, mark_value, coordinates):
        self.mark_value = mark_value
        self.coordinates = coordinates
