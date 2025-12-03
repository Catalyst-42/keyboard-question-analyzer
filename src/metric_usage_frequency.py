"""
Used to calculate layout finger usage and row usage.
"""

from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.setup import *

ARGS = setup('metric_usage_frequency')

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)

# Emulated by loading
print(keyboard.info(), '\n')
print(keyboard.keyboard_usage())

report = {
    'finger_usage_1': keyboard.finger_usage_frequency(1),
    'finger_usage_2': keyboard.finger_usage_frequency(2),
    'finger_usage_3': keyboard.finger_usage_frequency(3),
    'finger_usage_4': keyboard.finger_usage_frequency(4),
    'finger_usage_5': keyboard.finger_usage_frequency(5),
    'finger_usage_6': keyboard.finger_usage_frequency(6),
    'finger_usage_7': keyboard.finger_usage_frequency(7),
    'finger_usage_8': keyboard.finger_usage_frequency(8),
    'finger_usage_9': keyboard.finger_usage_frequency(9),
    'finger_usage_10': keyboard.finger_usage_frequency(10),
    'row_usage_k': keyboard.row_usage_frequency('K'),
    'row_usage_e': keyboard.row_usage_frequency('E'),
    'row_usage_d': keyboard.row_usage_frequency('D'),
    'row_usage_c': keyboard.row_usage_frequency('C'),
    'row_usage_b': keyboard.row_usage_frequency('B'),
    'row_usage_a': keyboard.row_usage_frequency('A'),
}

for feature in report:
    print(f'{feature}: {report[feature]:.2%}')
