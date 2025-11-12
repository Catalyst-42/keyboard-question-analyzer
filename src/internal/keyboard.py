from __future__ import annotations
from typing import Literal
from yaml import safe_load

from internal.key import Key
from internal.corpus import Corpus

class Keyboard():
    """Model of keyboard.

    Contain all information about keyboard and current layout.
    Can calculate information about keys using selected corpus.
    """

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

    def print_keyboard_usage(self):
        format_map = {"fingers": "Usage of fingers", "rows": "Usage of rows", "total": 0}
        hands_frequency = """\
        \r{fingers:^32}{rows:^19}
        \r
        \r ╭╴{l1:<6.2%}              {r10:>6.2%}╶╮      {o1}
        \r │ ╭╴{l2:<6.2%}          {r9:>6.2%}╶╮ │      {o2}
        \r 1 2 3 4                7 8 9 10     {o3}
        \r     │ ╰╴{l4:<6.2%}  {r7:>6.2%}╶╯ │          {o4}
        \r     ╰╴{l3:<6.2%}      {r8:>6.2%}╶╯          {o5}
        \r
        \r Left - {l:<6.2%}    {r:>6.2%} - Right     ∑ {total:.1%}
        \r"""

        def calculate_hand_uage(hand: Literal["left", "right"]):
            hand_frequency = 0
            fingers = range(1, 6, 1)

            finger_direction = 1 if hand == "left" else -1
            finger_offset = 1 if hand == "left" else 6

            for finger_index, _ in enumerate(fingers[::finger_direction], finger_offset):
                finger_frequency = sum([key.get_total_frequency() for key in self._mapping_to_key.values() if key.finger == finger_index])
                hand_frequency += finger_frequency

                format_map[f"{"l" if hand == "left" else "r"}{finger_index}"] = finger_frequency
            format_map["l" if hand == "left" else "r"] = hand_frequency

        calculate_hand_uage("left")
        calculate_hand_uage("right")

        def calculate_row_usage(row):
            row_usage = sum([
                key.get_total_frequency() for key in self.keyboard.values() if key.row == row
            ])

            format_map["total"] += row_usage
            format_map[f"o{row}"] = f"{row} {row_usage:.2%}" if row_usage != 0 else ""

        # Can display only first 6 rows
        for row in range(1, 6):
            calculate_row_usage(row)

        print(hands_frequency.format_map(format_map))

    def key_max_usage(self) -> int:
        if self._key_max_usage is None:
            self.prepare()

        return self._key_max_usage

    @property
    def usage(self) -> int:
        """Calculates total keyboard usage."""
        if self._usage is None:
            self.prepare()

        return self._usage

    def finger_usage(self, finger: int):
        """Calculates finger usage by mappings."""
        usage = 0

        for key in self.keys:
            if key.finger == finger:
                usage += key.usage

        return usage

    def finger_usage_percent(self, finger: int) -> int:
        return self.finger_usage(finger) / self.usage

    def hand_usage(self, hand: int):
        """Calculate hand usage by it's fingers."""
        usage = 0

        for finger in range(1, 11):
            if hand == 1 and finger <= 5:
                usage += self.finger_usage(finger)

            elif hand == 2 and finger > 5:
                usage += self.finger_usage(finger)

        return usage

    def hand_usage_frequency(self, hand: int) -> int:
        return self.hand_usage(hand) / self.usage

    def row_usage(self, row: int) -> int:
        """Calculate row usage by keys."""
        usage = 0

        for key in self.keys:
            if key.row == row:
                usage += key.usage

        return usage

    def row_usage_frequency(self, row: int) -> int:
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
