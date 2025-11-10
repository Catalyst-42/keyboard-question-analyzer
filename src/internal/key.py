from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from internal.keyboard import Keyboard

class Key():
    def __init__(self, keyboard: Keyboard, key_code: str, physical_key: dict, logical_key: dict):
        self.keyboard: Keyboard = keyboard

        # Key
        self.x: int = physical_key["x"]
        self.y: int = physical_key["y"]
        self.w: int = physical_key["w"]
        self.h: int = physical_key["h"]
        self.row: int = physical_key["row"]
        self.finger: int = physical_key.get("finger", 0)
        self.is_home: bool = physical_key.get("is_home", False)

        self.notch = False
        if notch := physical_key.get('notch'):
            self.notch = True
            self.notch_place = notch['place']
            self.notch_w = notch['w']
            self.notch_h = notch['h']

        # Layout
        self.key: str = key_code
        self.mappings: dict = logical_key.get("mappings", {1: '∅'})
        self.is_modifier: bool = logical_key.get("is_modifier", False)

    def __repr__(self):
        return f"Key {self.key}, at ({self.x}, {self.y}), {self.finger} finger, {self.row} row"

    def __eq__(self, other):
        if other is None:
            return False
        return self.key == other.key

    def get_mapping(self, layer: int) -> str:
        if layer > 0:
            return self.mappings.get(layer, self.mappings.get(layer - 1))

        raise ValueError(f"Layout mapping not found for {layer} layer")

    def get_frequency(self, layer: int):
        return self.keyboard.get_frequency(self.get_mapping(layer))

    def get_total_frequency(self):
        return sum([self.get_frequency(mapping) for mapping in self.mappings])

    def get_usage(self, layer):
        return self.keyboard.get_usage(self.get_mapping(layer))

    def visual_center(self):
        center_x = self.x + self.w/2
        center_y = -self.y - self.h/2

        if self.notch:
            center_x = self.x + self.w/2
            center_y = -self.y - self.notch_h/2

        return (center_x, center_y)
