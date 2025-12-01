from __future__ import annotations

from enum import IntEnum, StrEnum
from functools import cached_property
from collections import Counter

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

        self.one_unit: int = keyboard_model['one_unit']

        self.name = keyboard_model['name']
        self.file = keyboard_model['file']

        self.layout_name = layout_model['name']
        self.layout_file = layout_model['file']

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

        self.check_dublicate_mappings()

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

    def mapping_to_key(self, mapping: str) -> Key | None:
        """Return None or key that contain selected mapping."""
        return self._mapping_to_key.get(mapping)

    @property
    def keys(self) -> list[Key]:
        """Return list of keys on keyboard."""
        return list(self._code_to_key.values())

    @property
    def keys_is_home(self) -> list[Key]:
        """Return list of keys that marked as homerow."""
        return list(key for key in self.keys if key.is_home)

    def info(self) -> str:
        """Return names of keyboard, layout and corpus."""
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
        """Return filled template with keyboard usage stats."""
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

    @cached_property
    def key_max_usage(self) -> int:
        """Finds key, that used rather than all other ones."""
        self._key_max_usage = max(key.usage for key in self.keys)
        return self._key_max_usage

    @cached_property
    def usage(self) -> int:
        """Calculates total keyboard usage."""
        self._usage = 0
        for key in self.keys:
            self._usage += key.usage

        return self._usage

    def finger_usage(self, finger: Finger):
        """Calculates finger usage by mappings."""
        usage = 0

        for key in self.keys:
            if key.finger == finger:
                usage += key.usage

        return usage

    def finger_usage_frequency(self, finger: Finger) -> float:
        """Return finger usage float value."""
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
        """Return hand usage float value."""
        return self.hand_usage(hand) / self.usage

    def row_usage(self, row: Row) -> int:
        """Return row usage by keys."""
        usage = 0

        for key in self.keys:
            if key.row == row:
                usage += key.usage

        return usage

    def row_usage_frequency(self, row: Row) -> float:
        """Return selected row usage frequency."""
        return self.row_usage(row) / self.usage

    @property
    def chars(self) -> set:
        """Return set if chars, used in layout. Ignores modifiers."""
        mappings = set()

        for key in self.keys:
            if key.is_modifier:
                continue

            mappings.update(key.mappings.values())

        return mappings

    @cached_property
    def bigram_mean_distance(self) -> float:
        """Return mean distance between bigram keys."""
        bigrams = self.corpus.bigrams

        total_distance = 0
        total_weight = 0

        for bigram, weight in bigrams.items():
            left_key = self.mapping_to_key(bigram[0])
            right_key = self.mapping_to_key(bigram[-1])

            distance = left_key.distance_to(right_key) * weight

            total_distance += distance
            total_weight += weight

        return total_distance / total_weight / self.one_unit

    def is_sfb(self, bigram: str) -> bool:
        """True if bigram are same-finger one.

        Consider bigram as SFB if:
        - Characters pressed with same finger
        - Characters not equal (a.e. `ee` non an SFB)
        """
        assert len(bigram) == 2, 'bigram length must be 2'

        left_key = self.mapping_to_key(bigram[0])
        right_key = self.mapping_to_key(bigram[-1])

        # Same characters
        if bigram[0] == bigram[-1]:
            return False

        # No fingers found
        if not left_key or not right_key:
            return False

        return left_key.finger == right_key.finger

    def _ngram_frequency(self, ngrams: Counter, by: callable[str, bool]) -> float:
        """Counts frequency by function filter for ngram counter."""
        total_usage = 0

        for ngram, usage in ngrams.items():
            if by(ngram):
                total_usage += usage

        return total_usage / ngrams.total()

    @cached_property
    def same_finger_bigram_frequency(self) -> float:
        """Calculated same-finger bigram occurance frequency."""
        bigrams = self.corpus.bigrams
        return self._ngram_frequency(bigrams, self.is_sfb)

    @cached_property
    def same_finger_bigram_mean_distance(self) -> float:
        """Return mean distance between same-finger bigrams in units."""
        bigrams = self.corpus.bigrams

        total_distance = 0
        total_weight = 0

        for bigram, weight in bigrams.items():
            if not self.is_sfb(bigram):
                continue

            left_key = self.mapping_to_key(bigram[0])
            right_key = self.mapping_to_key(bigram[-1])

            distance = left_key.distance_to(right_key) * weight

            total_distance += distance
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_distance / total_weight / self.one_unit

    def _is_scissor_bigram(self, bigram: str, full: bool) -> bool:
        """True if bigram are half or full scissor one.

        Consider bigram as scissor if:
        - Bigram typed with one hand
        - The finger that prefers being higher are not
            - Prefered order (from top to bottom) are:
                - Middle
                - Ring
                - Pinky
                - Index
                - Thumb

        Consider bigram as half scissor if:
        - Vertical separation between keys
        is less than 2 units and more than one

        Consider bigram as full scissor if:
        - Vertical separation between keys is 2 or more units
        """
        assert len(bigram) == 2, 'bigram length must be 2'
        top_key = self.mapping_to_key(bigram[0])
        bottom_key = self.mapping_to_key(bigram[-1])

        # Keys not found
        if not top_key or not bottom_key:
            return False

        # Must be different fingers
        if top_key.finger == bottom_key.finger:
            return False

        # Must be one hand fingers
        if top_key.hand != bottom_key.hand:
            return False

        # Must be around 2u of distance for full
        distance = abs(top_key.y - bottom_key.y) / self.one_unit
        if full:
            if distance < 2:
                return False

        # Must be around 1u of distance for half
        if not full:
            if distance < 1 or distance >= 2:
                return False

        # Lower index means the higher must be finger
        order = {
            Keyboard.Finger.RIGHT_MIDDLE: 0, 
            Keyboard.Finger.RIGHT_RING: 1,
            Keyboard.Finger.RIGHT_PINKY: 2,
            Keyboard.Finger.RIGHT_INDEX: 3,
            Keyboard.Finger.RIGHT_THUMB: 4,

            Keyboard.Finger.LEFT_MIDDLE: 0,
            Keyboard.Finger.LEFT_RING: 1,
            Keyboard.Finger.LEFT_PINKY: 2,
            Keyboard.Finger.LEFT_INDEX: 3,
            Keyboard.Finger.LEFT_THUMB: 4,
        }

        # Determine which key finger must be higher
        if order[top_key.finger] > order[bottom_key.finger]:
            top_key, bottom_key = bottom_key, top_key

        return not (top_key.y < bottom_key.y)

    def is_fsb(self, bigram: str) -> bool:
        """True if bigram are full scissor one."""
        return self._is_scissor_bigram(bigram, True)

    def is_hsb(self, bigram: str) -> bool:
        """True if bigram are half scissor one."""
        return self._is_scissor_bigram(bigram, False)

    def is_lsb(self, bigram: str) -> bool:
        """True if bigram are lateral stretch.

        Consider bigram as lateral stretch if:
        - Bigram typed with adjasent or semi-adjasent fingers
        - Adjasent finger horisontal distance more than 2 units
        - Or semi-adjasent horisontal finger distance more than 3.5 units
        """
        assert len(bigram) == 2, 'bigram length must be 2'
        left_key = self.mapping_to_key(bigram[0])
        right_key = self.mapping_to_key(bigram[-1])

        # Keys not found
        if not left_key or not right_key:
            return False

        # Must be one hand fingers
        if left_key.hand != right_key.hand:
            return False

        # Get adjasments
        finger_distance = left_key.finger - right_key.finger

        adjasent = True if finger_distance == 1 else False
        semi_adjasent = True if finger_distance == 2 else False

        # Get treshold by adjasment
        if adjasent:
            treshlod = 2
        elif semi_adjasent:
            treshlod = 3.5
        else:
            return False

        distance = abs(left_key.x - right_key.x)
        return distance / self.one_unit >= treshlod

    @cached_property
    def full_scissor_bigram_frequency(self) -> float:
        """Calculates full scissor bigrams occurance frequency."""
        bigrams = self.corpus.bigrams
        return self._ngram_frequency(bigrams, self.is_fsb)

    @cached_property
    def half_scissor_bigram_frequency(self) -> float:
        """Calculates half scissor bigrams occurance frequency."""
        bigrams = self.corpus.bigrams
        return self._ngram_frequency(bigrams, self.is_hsb)

    @cached_property
    def lateral_stretch_bigram_frequency(self) -> float:
        """Calculates lateral stretch bigram occurance frequency."""
        bigrams = self.corpus.bigrams
        return self._ngram_frequency(bigrams, self.is_lsb)

    @cached_property
    def lateral_stretch_skipgram_frequency(self) -> float:
        """Calculates lateral stretch 1-skipgram occurance frequency."""
        lsb = 0
        trigrams = self.corpus.trigrams

        for trigram, usage in trigrams.items():
            bigram = trigram[0] + trigram[2]
            if self.is_lsb(bigram):
                lsb += usage

        return lsb / trigrams.total()

    def is_sfs(self, trigram: str) -> bool:
        """True if trigram are same-finger 1-skipgram.

        Consider trigram as same-finger 1-skipgramm if:
        - First and last characters are pressed by same finger
        - First and last charactes are not the same (a.e. `e_e` not an SFS)
        - Middle characted doesn't matters
        """
        assert len(trigram) == 3, 'trigram length must be 3'

        left_key = self.mapping_to_key(trigram[0])
        right_key = self.mapping_to_key(trigram[2])

        # Same characters
        if trigram[0] == trigram[2]:
            return False

        # No fingers found
        if not left_key or not right_key:
            return False

        return left_key.finger == right_key.finger

    def is_alternate(self, trigram: str) -> bool:
        """True if trigram are alternate hand typed.

        Consider trigram as alternate if:
        - First characted typed with one hand
        - Second characted typed with another hand
        - Third characted typed again with one (first) hand
        """
        assert len(trigram) == 3, 'trigram length must be 3'
        first_key = self.mapping_to_key(trigram[0])
        second_key = self.mapping_to_key(trigram[1])
        third_key = self.mapping_to_key(trigram[2])

        # Keys not found
        if not all([first_key, second_key, third_key]):
            return False

        return (
            first_key.hand == third_key.hand
            and first_key.hand != second_key.hand
        )

    def is_roll(self, trigram: str) -> bool:
        """True if trigram are two keys rolled.

        Consider trigram as rolled if:
        - Pressing two keys with one hand and other with another
        - Same pressed pair must be typed with different fingers
        """
        assert len(trigram) == 3, 'trigram length must be 3'
        first_key = self.mapping_to_key(trigram[0])
        second_key = self.mapping_to_key(trigram[1])
        third_key = self.mapping_to_key(trigram[2])

        # Keys not found
        if not all([first_key, second_key, third_key]):
            return False

        return ((
                # First and second keys are roll
                first_key.hand == second_key.hand
                and first_key.finger != second_key.finger
                and first_key.hand != third_key.hand
            ) or (
                # Second and third keys are roll
                second_key.hand == third_key.hand
                and second_key.finger != third_key.finger
                and second_key.hand != first_key.hand
            )
        )

    def _is_shdf(self, f1: Key, f2: Key, f3: Key) -> bool:
        """True if keys same hand and typed with different fingers."""
        # Keys not found
        if not all([f1, f2, f3]):
            return False

        # One hand
        if not (f1.hand == f2.hand == f3.hand):
            return False

        # Equal fingers
        return (
            f1.finger != f2.finger
            and f2.finger != f3.finger
            and f1.finger != f3.finger
        )

    def is_onehand(self, trigram: str) -> bool:
        """True if trigram are onehand rolled (3roll).

        Consider trigram as onehand if:
        - All characters typed with one hand
        - All characters typed with different fingers
        - All keys goes in same direction
        """
        assert len(trigram) == 3, 'trigram length must be 3'
        first_key = self.mapping_to_key(trigram[0])
        second_key = self.mapping_to_key(trigram[1])
        third_key = self.mapping_to_key(trigram[2])

        if not self._is_shdf(first_key, second_key, third_key):
            return False

        direction_12 = first_key.finger > second_key.finger
        direction_23 = second_key.finger > third_key.finger

        return (
            direction_12 == direction_23
        )

    def is_redirect(self, trigram: str) -> bool:
        """True if trigram are redirect one.

        Consider trigram as redirect if:
        - All characters typed with one hand
        - All characters typed with different fingers
        - Direction of typing first 2 characters don't match last 2
        """
        assert len(trigram) == 3, 'trigram length must be 3'
        first_key = self.mapping_to_key(trigram[0])
        second_key = self.mapping_to_key(trigram[1])
        third_key = self.mapping_to_key(trigram[2])

        if not self._is_shdf(first_key, second_key, third_key):
            return False

        direction_12 = first_key.finger > second_key.finger
        direction_23 = second_key.finger > third_key.finger

        return (
            direction_12 != direction_23
        )

    @cached_property
    def same_finger_skipgram_frequency(self) -> float:
        """Return same-finger 1-skipgram occurance frequency."""
        trigrams = self.corpus.trigrams
        return self._ngram_frequency(trigrams, self.is_sfs)

    @cached_property
    def same_finger_skipgram_mean_distance(self) -> float:
        """Return mean distance between same-finger 1-skipgram in units."""
        trigrams = self.corpus.trigrams

        total_distance = 0
        total_weight = 0

        for trigram, weight in trigrams.items():
            if not self.is_sfs(trigram):
                continue

            left_key = self.mapping_to_key(trigram[0])
            right_key = self.mapping_to_key(trigram[2])

            distance = left_key.distance_to(right_key) * weight

            total_distance += distance
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_distance / total_weight / self.one_unit

    @cached_property
    def full_scissor_skipgram_frequency(self) -> float:
        """Calculates full scissor 1-skipgram occurance frequency."""
        fss = 0
        trigrams = self.corpus.trigrams

        for trigram, usage in trigrams.items():
            bigram = trigram[0] + trigram[2]
            if self.is_fsb(bigram):
                fss += usage

        return fss / trigrams.total()

    @cached_property
    def half_scissor_skipgram_frequency(self) -> float:
        """Calculates half scissor 1-skipgram occurance frequency."""
        hss = 0
        trigrams = self.corpus.trigrams

        for trigram, usage in trigrams.items():
            bigram = trigram[0] + trigram[2]
            if self.is_hsb(bigram):
                hss += usage

        return hss / trigrams.total()

    @cached_property
    def alternate_frequency(self) -> float:
        """Return alternate trigram occurance frequency."""
        trigrams = self.corpus.trigrams
        return self._ngram_frequency(trigrams, self.is_alternate)

    @cached_property
    def roll_frequency(self) -> float:
        """Return roll (2roll) trigram occurance frequency."""
        trigrams = self.corpus.trigrams
        return self._ngram_frequency(trigrams, self.is_roll)

    @cached_property
    def onehand_frequency(self) -> float:
        """Return onehand (3roll) trigram occurance frequency."""
        trigrams = self.corpus.trigrams
        return self._ngram_frequency(trigrams, self.is_onehand)

    @cached_property
    def redirect_frequency(self) -> float:
        """Return redirect trigram occurance frequency."""
        trigrams = self.corpus.trigrams
        return self._ngram_frequency(trigrams, self.is_redirect)
