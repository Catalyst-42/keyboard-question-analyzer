from internal.keyboard import Key, Keyboard

class Finger():
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.active_key = None

    def goto(self, key: Key) -> int:
        new_x = key.x
        new_y = key.y

        distance = ((new_x - self.x)**2 + (new_y - self.y)**2) ** 0.5

        self.x = new_x
        self.y = new_y
        self.active_key = key

        return distance

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Hands():
    def __init__(self):
        self.fingers = {
            1: Finger(),
            2: Finger(),
            3: Finger(),
            4: Finger(),
            5: Finger(),
            6: Finger(),
            7: Finger(),
            8: Finger(),
            9: Finger(),
            10: Finger()
        }

    def goto_homerow(self, keyboard: Keyboard):
        for key in keyboard.keys:
            if key.is_home:
                self.fingers[key.finger].x = key.x
                self.fingers[key.finger].y = key.y

    def goto(self, finger, key) -> int:
        return self.fingers[finger].goto(key);

    def get_active_keys(self) -> list[Key]:
        return [self.fingers[finger].active_key for finger in self.fingers]

    def __repr__(self):
        finger_reprs = []
        for finger in self.fingers:
            finger_reprs.append(f"{finger}: {self.fingers[finger].__repr__()}")

        return "\n".join(finger_reprs)
