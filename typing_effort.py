from keyboard import Key, Keyboard
from setup import *


class Finger():
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def goto(self, key: Key):
        new_x = key.x
        new_y = key.y

        distance = ((new_x - self.x)**2 + (new_y - self.y)**2) ** 0.5

        self.x = new_x
        self.y = new_y

        return distance

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Fingers():
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

ARGS = setup("display")
fingers = Fingers()
keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])

fingers.goto_homerow(keyboard)
