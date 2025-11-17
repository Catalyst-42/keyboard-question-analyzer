from __future__ import annotations

from math import hypot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from internal.keyboard import Keyboard

class Key():
    """Model of keyboard key.

    Contains physical information and layout one.
    """

    def __init__(self, keyboard: Keyboard, key_code: str, key_data: dict, key_layout: dict):
        """Create key by given code, key data and layout data."""
        self.keyboard: Keyboard = keyboard
        self.key: str = key_code

        # Physical key properties
        self.x: int = key_data.get('x', 0)
        self.y: int = key_data.get("y", 0)
        self.w: int = key_data.get('w', 40)
        self.h: int = key_data.get('h', 40)
        self.row: Keyboard.Row = key_data.get('row', 'A')
        self.finger: Keyboard.Finger = key_data.get('finger', 1)
        self.hand: Keyboard.Hand = 'left' if self.finger < 6 else 'right'
        self.is_home: bool = key_data.get('is_home', False)

        # Notch params for curve enter key
        notch = key_data.get('notch', False)

        if notch:
            self.notch = True
            self.notch_place = notch.get('place')
            self.notch_w = notch.get('w', 40)
            self.notch_h = notch.get('h', 40)
        else:
            self.notch = False

        # Layout properties
        self.mappings: dict = key_layout.get('mappings', {})
        self.is_modifier: bool = key_layout.get('is_modifier', False)

    def __repr__(self) -> str:
        """Display key physical features: x, y finger and row."""
        return f'Key {self.key}, at ({self.x}, {self.y}), {self.finger} finger, {self.row} row'

    def mapping(self, layer: int) -> str:
        """Finds mapping by layer. Fallback on bottom layers if not found."""
        if layer > 0:
            return self.mappings.get(
                layer,
                self.mappings.get(layer - 1)  # Fallback on lower layer
            )

        print(f'Warning: key {self.key} is not mapped')
        return ''

    def layer_usage(self, layer: int) -> int:
        """Returns mapping usage by selected layer."""
        if self.is_modifier:
            return 0

        mapping = self.mapping(layer)
        return self.keyboard.corpus.char_usage(mapping)

    @property
    def usage(self) -> int:
        """Returns key total usage by all layers."""
        usage = 0
        for layer in self.mappings.keys():
            usage += self.layer_usage(layer)

        return usage

    def layer_frequency(self, layer: int) -> float:
        """Return key mapping usage by selected layer."""
        return self.layer_usage(layer) / self.keyboard.usage 

    @property
    def frequency(self) -> float:
        """Returns key total usage frequency by all layers."""
        return self.usage / self.keyboard.usage

    def visual_center(self) -> tuple[float, float]:
        """Return center of key in pixels (x, y). Balances for notch keys."""
        center_x = self.x + self.w/2
        center_y = self.y + self.h/2

        if self.notch:
            center_x = self.x + self.w/2
            center_y = self.y + self.notch_h/2

        return (center_x, center_y)

    def center(self) -> tuple[float, float]:
        """Calculates real key center (x, y) in pixels."""
        return (self.x + self.w/2, self.y + self.h/2)

    def distance_to(self, other: Key) -> float:
        """Calculated distance to other key in pixels."""
        ax, ay = self.center()
        bx, by = other.center()

        return hypot(
            ax - bx,
            ay - by
        )
