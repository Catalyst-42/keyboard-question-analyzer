from __future__ import annotations
from typing import Literal
from yaml import safe_load

from internal.key import Key
from internal.corpus import Corpus

class Keyboard():
    def __init__(self, keyboard: dict, layout: dict, corpus: Corpus):
        # self.frequencies = keys_frequencies["frequencies"]
        # self.total = sum(keys_frequencies["frequencies"].values())
        self.corpus = corpus

        self.keyboard: dict[str, Key] = {}
        self._mapping_to_key: dict[str, Key] = {}

        for key_code in keyboard["keyboard"]:
            key_key = keyboard['keyboard'][key_code]
            key_layout = layout["layout"].get(key_code, {})

            key_obj = Key(self, key_code, key_key, key_layout)
            self.keyboard[key_code] = key_obj

            for mapping_value in key_layout.get("mappings", {}).values():
                self._mapping_to_key[mapping_value] = key_obj

        self.check_unique_keys()

    @classmethod
    def load(self, keyboard_model: str, layout_model: str, corpus: str):
        keyboard_model: dict = safe_load(open(keyboard_model, encoding="utf-8").read())
        layout_model: dict = safe_load(open(layout_model, encoding="utf-8").read())
        # corpus = Corpus.load(corpus)
        corpus: dict = safe_load(open(corpus, encoding="utf-8").read())

        return Keyboard(keyboard_model, layout_model, corpus)

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

    def key_for(self, mapping):
        return self._mapping_to_key.get(mapping, None)
