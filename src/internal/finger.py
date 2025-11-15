from internal.key import Key
from internal.keyboard import Keyboard
from math import hypot

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
        """Move finger to center of selected key."""
        cx, cy = key.center()

        self.travel_distance += hypot(
            cx - self.x,
            cy - self.y
        )

        self.x = cx
        self.y = cy

    def __repr__(self) -> str:
        """Display finger position."""
        return f'({self.x}, {self.y})'
