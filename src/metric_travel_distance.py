"""
Used to calculate travel distance of layout.
"""

from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_travel_distance')

corpus = Corpus.load(ARGS['corpus'])
# corpus = Corpus('custom', 'привет')
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

# Emulate
print(keyboard.info(), '\n')
hands.simulate_typing(keyboard, corpus)

report = {
    'travel_distance': hands.travel_distance,
    'travel_distance_finger_1': hands.fingers[1].travel_distance,
    'travel_distance_finger_2': hands.fingers[2].travel_distance,
    'travel_distance_finger_3': hands.fingers[3].travel_distance,
    'travel_distance_finger_4': hands.fingers[4].travel_distance,
    'travel_distance_finger_5': hands.fingers[5].travel_distance,
    'travel_distance_finger_6': hands.fingers[6].travel_distance,
    'travel_distance_finger_7': hands.fingers[7].travel_distance,
    'travel_distance_finger_8': hands.fingers[8].travel_distance,
    'travel_distance_finger_9': hands.fingers[9].travel_distance,
    'travel_distance_finger_10': hands.fingers[10].travel_distance,
}

for feature in report:
    print(f'{feature}: {round((report[feature] / keyboard.one_unit)):,}u')

print()

for feature in report:
    print(f'mean_{feature}: {(report[feature] / keyboard.one_unit / corpus.length):.2}u')
