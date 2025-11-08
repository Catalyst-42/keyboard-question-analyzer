from internal.keyboard import Key

class Finger:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.travel_distance = 0.0

    def move_to(self, key: Key) -> float:
        new_x = key.x
        new_y = key.y

        distance = ((new_x - self.x)**2 + (new_y - self.y)**2) ** 0.5
        self.travel_distance += distance

        self.x = new_x
        self.y = new_y

        return distance

    def __repr__(self):
        return f"({self.x}, {self.y})"
