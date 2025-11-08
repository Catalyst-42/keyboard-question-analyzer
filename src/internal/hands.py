from internal.finger import Finger
from internal.keyboard import Key, Keyboard


class Hands:
    def __init__(self, keyboard: Keyboard):
        self.fingers = {
            i: Finger() for i in range(1, 11)
        }

        # Set position of keys on homerow
        for key in keyboard.keys:
            if key.is_home:
                self.fingers[key.finger].x = key.x
                self.fingers[key.finger].y = key.y

    def move_to(self, finger, key) -> float:
        return self.fingers[finger].move_to(key)

    def get_travel_distance(self, start_finger: int, end_finger: int) -> float:
        total = 0.0
        for finger_num in range(start_finger, end_finger + 1):
            total += self.fingers[finger_num].travel_distance
        return total

    def get_left_hand_travel_distance(self) -> float:
        return self.get_travel_distance(1, 5)

    def get_right_hand_travel_distance(self) -> float:
        return self.get_travel_distance(6, 10)

    def get_total_travel_distance(self) -> float:
        return (self.get_left_hand_travel_distance()
                + self.get_right_hand_travel_distance())

    def __repr__(self):
        finger_reprs = []
        for finger in self.fingers:
            finger_reprs.append(f"{finger}: {self.fingers[finger]}")
        return "\n".join(finger_reprs)
