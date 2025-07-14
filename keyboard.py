from __future__ import annotations
from typing import Literal

from yaml import safe_load


class Key():
    def __init__(self, keyboard: Keyboard, physical_key: dict, logical_key: dict):
        self.keyboard: Keyboard = keyboard

        # Physical keyboard
        self.key = physical_key["key"]
        self.x: int = physical_key["x"]
        self.y: int = physical_key["y"]
        self.w: int = physical_key["w"]
        self.h: int = physical_key["h"]
        self.row: int = physical_key["row"]
        self.finger: int = physical_key.get("finger", 0)
        self.is_home: bool = physical_key.get("is_home", False)

        # Logical keyboard
        self.key: str = logical_key["key"]
        self.mappings: dict = logical_key["mappings"]
        self.is_modifier: bool = logical_key.get("is_modifier", False)

    def get_mapping(self, layer: int):
        if layer > 0:
            return self.mappings.get(layer, self.mappings.get(layer - 1))
        raise ValueError(f"Layout mapping not found for {layer} layer")

    def get_frequency(self, layer: int):
        return self.keyboard.get_frequency(self.get_mapping(layer))

    def get_total_frequency(self):
        return sum([self.get_frequency(mapping) for mapping in self.mappings])

    def get_usage(self, layer):
        return self.keyboard.get_usage(self.get_mapping(layer))


class Keyboard():
    def __init__(self, physical_layout: dict, logical_layout: dict, keys_frequencies: dict):
        self.frequencies = keys_frequencies["frequencies"]
        self.total = sum(keys_frequencies["frequencies"].values())

        self.keyboard: dict[str, Key] = {}
        for physical_key in physical_layout["keyboard"]:
            for logical_key in logical_layout["layout"]:
                if physical_key["key"] == logical_key["key"]:
                    self.keyboard[physical_key["key"]] = Key(self, physical_key, logical_key)
                    break

        # Ensure that layout mapped properly
        self.check_unique_keys()

    @classmethod
    def load(self, physical_layout: str, logical_layout: str, keys_frequencies: str):
        physical_layout: dict = safe_load(open(physical_layout, encoding="utf-8").read())
        logical_layout: dict = safe_load(open(logical_layout, encoding="utf-8").read())
        keys_frequencies: dict = safe_load(open(keys_frequencies, encoding="utf-8").read())

        return Keyboard(physical_layout, logical_layout, keys_frequencies)

    @property
    def keys(self) -> list[Key]:
        return self.keyboard.values()

    def check_unique_keys(self):
        dublicates_found = False
        mappings = set()
        for key in self.keys:
            if key.is_modifier:
                continue

            for mapping in key.mappings.values():
                if mapping not in mappings:
                    mappings.add(mapping)
                else:
                    dublicates_found = True
                    print(f"Warning: mapping \"{mapping}\" repeats on layout more than once")

        if dublicates_found:
            print()

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
                finger_frequency = sum([key.get_total_frequency() for key in self.keyboard.values() if key.finger == finger_index])
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

    def get_frequency(self, mapping: str):
        return self.frequencies.get(mapping, 0) / self.total

    def get_max_frequency(self):
        return max(self.frequencies.values) / self.total

    def get_usage(self, mapping: str):
        return self.frequencies.get(mapping, 0)

    def get_max_usage(self):
        return max(self.frequencies.values())

    @property
    def mappings(self):
        mappings = set()
        for key in self.keys:
            if key.is_modifier:
                continue

            mappings.update(key.mappings.values())

        return mappings
