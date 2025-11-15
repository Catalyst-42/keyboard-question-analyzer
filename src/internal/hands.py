from internal.finger import Finger
from internal.key import Key
from internal.keyboard import Keyboard
from internal.corpus import Corpus


class Hands:
    """Model of hands that type text.

    Used in evaluation of finger travel distance.
    """

    def __init__(self, keyboard: Keyboard) -> None:
        """Initialize hands on keyboard."""
        # 1 - left pinky
        # 2 - left ring
        # etc
        self._fingers: dict[Keyboard.Finger, Finger] = {
            i: Finger(i) for i in Keyboard.Finger
        }

        # Set position of keys on homerow
        for key in keyboard.keys_is_home:
            cx, cy = key.center()
            self._fingers[key.finger].x = cx
            self._fingers[key.finger].y = cy

    def __repr__(self) -> str:
        """Return positions of all fingers of both hands."""
        finger_reprs = []
        for finger in self._fingers:
            finger_reprs.append(f"{finger}: {self._fingers[finger]}")

        return "\n".join(finger_reprs)

    @property
    def fingers(self) -> dict[Keyboard.Finger, Finger]:
        """Return list of fingers of both hands."""
        return self._fingers

    def _travel_distance(self, start: int = None, end: int = None) -> float:
        """Get travel distance of selected keys."""
        fingers = list(self.fingers.values())
        distance = sum(
            finger.travel_distance for finger in fingers[start:end]
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

    def move_to(self, finger: Keyboard.Finger, key: Key) -> float:
        """Move finger to selected key."""
        return self._fingers[finger].move_to(key)

    def simulate_typing(self, keyboard: Keyboard, corpus: Corpus) -> None:
        """Calculates travel distance by typing emulation."""
        one_percent = corpus.length // 100 - 1

        for i, char in enumerate(corpus.text):
            key = keyboard.key_by_mapping(char)

            if key: 
                self.move_to(key.finger, key)

            if i % one_percent == 0:
                print(f'\rProgress: {i/corpus.length:.0%} ', end='')

        print('\n')
