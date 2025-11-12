from internal.keyboard import Key

class Finger:
    """Model if finger that types text.
    
    Used in travel distance evaluation.
    """

    def __init__(self, index: int = 0, x: int = 0, y: int = 0):
        """Initialize finger."""
        self.index = index
        self.x = x
        self.y = y

        self.travel_distance = 0.0

    def move_to(self, key: Key) -> float:
        """Move finger to selected position."""
        new_x = key.x
        new_y = key.y

        distance = ((new_x - self.x)**2 + (new_y - self.y)**2) ** 0.5
        self.travel_distance += distance

        self.x = new_x
        self.y = new_y

        return distance

    def __repr__(self):
        """Display finger position."""
        return f'({self.x}, {self.y})'
