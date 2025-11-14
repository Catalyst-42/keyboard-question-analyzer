from __future__ import annotations

from enum import IntEnum, StrEnum

from yaml import safe_load

from internal.corpus import Corpus
from internal.key import Key


class Keyboard():
    """Model of keyboard.

    Contain all information about keyboard and current layout.
    Can calculate information about keys using selected corpus.
    """

    class Row(StrEnum):
        """Enumeration for row index according to W3C standard."""
        K = 'K'
        E = 'E'
        D = 'D'
        C = 'C'
        B = 'B' 
        A = 'A'

    class Finger(IntEnum):
        """Enumeration for keyboard fingers."""
        LEFT_PINKY = 1
        LEFT_RING = 2
        LEFT_MIDDLE = 3
        LEFT_INDEX = 4
        LEFT_THUMB = 5
        RIGHT_THUMB = 6 
        RIGHT_INDEX = 7
        RIGHT_MIDDLE = 8
        RIGHT_RING = 9
        RIGHT_PINKY = 10

    class Hand(StrEnum):
        LEFT = 'left'
        RIGHT = 'right'

    def __init__(self, keyboard_model: dict, layout_model: dict, corpus: Corpus):
        """Init keyboard. Uses corpus to calculate usages."""
        self.corpus = corpus

        self.name = keyboard_model['name']
        self.layout_name = layout_model['name']

        self._code_to_key: dict[str, Key] = {}
        self._mapping_to_key: dict[str, Key] = {}

        keys: dict = keyboard_model.get('keyboard')
        layouts: dict = layout_model.get('layout')

        for key_code, key_data in keys.items():
            key_layout = layouts.get(key_code, {})
            key_chars = key_layout.get("mappings", {}).values()

            key = Key(self, key_code, key_data, key_layout)

            # Map by code and chars on layout
            self._code_to_key[key_code] = key
            for char in key_chars:
                self._mapping_to_key[char] = key

        # Cached values
        self._usage: int | None = None
        self._key_max_usage: int | None = None 

        self.check_dublicate_mappings()

    def prepare(self):
        """Calculate keyboard stats."""
        self._key_max_usage = max(key.usage for key in self.keys)
        self._usage = 0

        for key in self.keys:
            self._usage += key.usage

    def _drop_cache(self):
        """Drops cached properties."""
        self._key_max_usage = None

    @classmethod
    def load(self, keyboard_model_path, layout_model_path, corpus: Corpus):
        """Load keyboard from YAML models."""
        keyboard_model: dict = safe_load(
            open(keyboard_model_path, encoding="utf-8").read()
        )
        layout_model: dict = safe_load(
            open(layout_model_path, encoding="utf-8").read()
        )

        return Keyboard(keyboard_model, layout_model, corpus)

    def key_by_mapping(self, mapping: str) -> Key:
        """Returns keyboard key that contain selected mapping."""
        return self._mapping_to_key.get(mapping)

    @property
    def keys(self) -> list[Key]:
        """Returns list of keys on keyboard."""
        return list(self._code_to_key.values())

    @property
    def keys_is_home(self) -> list[Key]:
        """Returns list of keys that marked as homerow."""
        return list(key for key in self.keys if key.is_home)

    def info(self) -> str:
        """Returns names of keyboard, layout and corpus."""
        return (
            f'Keyboard: {self.name}\n'
            f'Layout: {self.layout_name}\n'
            f'Corpus: {self.corpus.name}'
        )

    def check_dublicate_mappings(self):
        """Checks if there's dublicated of mapping on keyboard."""
        dublicates = set()
        chars = set()

        for key in self.keys:
            if key.is_modifier:
                continue

            for mapping in key.mappings.values():
                if mapping not in chars:
                    chars.add(mapping)
                else:
                    dublicates.add(mapping)

        for dublicate in dublicates:
            print(f'Warning: mapping "{dublicate}" repeats on layout')

    def keyboard_usage(self):
        """Returns filled template with keyboard usage stats."""
        format_map = {
            "fingers": "Usage of fingers",
            "rows": "Usage of rows", "total": 0
        }

        hands_frequency = """\
        \r{fingers:^32}{rows:^19}
        \r
        \r ╭╴{f1:<6.2%}              {f10:>6.2%}╶╮      {rE:.2%}
        \r │ ╭╴{f2:<6.2%}          {f9:>6.2%}╶╮ │      {rD:.2%}
        \r 1 2 3 4                7 8 9 10     {rC:.2%}
        \r     │ ╰╴{f4:<6.2%}  {f7:>6.2%}╶╯ │          {rB:.2%}
        \r     ╰╴{f3:<6.2%}      {f8:>6.2%}╶╯          {rA:.2%}
        \r
        \r Left - {l:<6.2%}    {r:>6.2%} - Right
        \r"""

        for finger in Keyboard.Finger:
            format_map[f'f{finger}'] = self.finger_usage_frequency(finger)

        for row in Keyboard.Row:
            format_map[f'r{row}'] = self.row_usage_frequency(row)

        format_map['l'] = self.hand_usage_frequency('left')
        format_map['r'] = self.hand_usage_frequency('right')

        return hands_frequency.format_map(format_map)

    def key_max_usage(self) -> int:
        """Finds key, that used rather than all other ones."""
        if self._key_max_usage is None:
            self.prepare()

        return self._key_max_usage

    @property
    def usage(self) -> int:
        """Calculates total keyboard usage."""
        if self._usage is None:
            self.prepare()

        return self._usage

    def finger_usage(self, finger: Finger):
        """Calculates finger usage by mappings."""
        usage = 0

        for key in self.keys:
            if key.finger == finger:
                usage += key.usage

        return usage

    def finger_usage_frequency(self, finger: Finger) -> float:
        """Returns finger usage float value."""
        return self.finger_usage(finger) / self.usage

    def hand_usage(self, hand: Hand) -> int:
        """Calculate hand usage by it's fingers."""
        usage = 0

        for finger in range(1, 11):
            if hand == 'left' and finger <= 5:
                usage += self.finger_usage(finger)

            elif hand == 'right' and finger > 5:
                usage += self.finger_usage(finger)

        return usage

    def hand_usage_frequency(self, hand: Hand) -> float:
        """Returns hand usage float value."""
        return self.hand_usage(hand) / self.usage

    def row_usage(self, row: Row) -> int:
        """Returns row usage by keys."""
        usage = 0

        for key in self.keys:
            if key.row == row:
                usage += key.usage

        return usage

    def row_usage_frequency(self, row: Row) -> float:
        """Returns selected row usage frequency."""
        return self.row_usage(row) / self.usage

    @property
    def chars(self):
        """Returns list if chars, used in layout. Ignores modifiers."""
        mappings = set()

        for key in self.keys:
            if key.is_modifier:
                continue

            mappings.update(key.mappings.values())

        return mappings
