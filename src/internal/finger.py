from internal.key import Key
from internal.keyboard import Keyboard

class Finger:
    """Model if finger that types text.

    Used in travel distance evaluation.
    """

    def __init__(self, index: Keyboard.Finger, x: int = 0, y: int = 0) -> None:
        """Initialize finger."""
        self.index = index
        self.x = x
        self.y = y

        self.travel_distance = 0.0

    def move_to(self, key: Key) -> None:
        """Move finger to selected position."""
        self.travel_distance += (
            ((key.x - self.x)**2 + (key.y - self.y)**2) ** 0.5 
        )

        self.x = key.x
        self.y = key.y

    def __repr__(self) -> str:
        """Display finger position."""
        return f'({self.x}, {self.y})'
