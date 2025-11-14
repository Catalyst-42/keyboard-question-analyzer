from internal.finger import Finger
from internal.keyboard import Keyboard


class Hands:
    """Model of hands that type text.

    Used in evaluation of finger travel distance.
    """

    def __init__(self, keyboard: Keyboard):
        """Initialize hands on keyboard."""
        # 1 - left pinky
        # 2 - left ring
        # etc
        self._fingers = {
            i: Finger(i) for i in range(1, 11)
        }

        # Set position of keys on homerow
        for key in keyboard.keys_is_home:
            self._fingers[key.finger].x = key.x
            self._fingers[key.finger].y = key.y

    @property
    def fingers(self) -> list[Finger]:
        """Return list of fingers of both hands."""
        return list(self._fingers.values())

    def move_to(self, finger, key) -> float:
        """Move finger to selected key."""
        return self._fingers[finger].move_to(key)

    def _travel_distance(self, start: int = None, end: int = None) -> float:
        """Get travel distance of selected keys."""
        distance = sum(
            finger.travel_distance for finger in self.fingers[start:end]
        )

        return distance

    @property
    def travel_distance_left_hand(self) -> float:
        """Get travel distance for left hand."""
        return self._travel_distance(end=5)

    @property
    def travel_distance_right_hand(self) -> float:
        """Get travel distance for right hand."""
        return self._travel_distance(start=5)

    @property
    def travel_distance(self) -> float:
        """Get total travel distance."""
        return self._travel_distance()

    def __repr__(self):
        """Return positions of all fingers of both hands."""
        finger_reprs = []
        for finger in self._fingers:
            finger_reprs.append(f"{finger}: {self._fingers[finger]}")

        return "\n".join(finger_reprs)
