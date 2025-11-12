from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_finger_usage')

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

print(keyboard.info(), '\n')

report = {
    'Keyboard': keyboard.name,
    'Corpus': corpus.name,
    'Layout': keyboard.layout_name,
    'Frequency heatmap': '',  # TODO
    'Hand usage left hand': keyboard.hand_usage_frequency(1),
    'Hand usage right hand': keyboard.hand_usage_frequency(2),
    'Finger usage 1': keyboard.finger_usage_percent(1),
    'Finger usage 2': keyboard.finger_usage_percent(2),
    'Finger usage 3': keyboard.finger_usage_percent(3),
    'Finger usage 4': keyboard.finger_usage_percent(4),
    'Finger usage 5': keyboard.finger_usage_percent(5),
    'Finger usage 6': keyboard.finger_usage_percent(6),
    'Finger usage 7': keyboard.finger_usage_percent(7),
    'Finger usage 8': keyboard.finger_usage_percent(8),
    'Finger usage 9': keyboard.finger_usage_percent(9),
    'Finger usage 10': keyboard.finger_usage_percent(10),
    'Row usage top': keyboard.row_usage_frequency('top'),
    'Row usage home': keyboard.row_usage_frequency('home'),
    'Row usage bottom': keyboard.row_usage_frequency('bottom'),
    'Scissor bigrams left hand': 0,  # TODO
    'Scissor bigrams right hand': 0,  # TODO
    'Same finger bigrams left hand': 0,  # TODO
    'Same finger bigrams right hand': 0,  # TODO
    'Alternating finger bigrams left hand': 0,  # TODO
    'Alternating finger bigrams right hand': 0,  # TODO
    'Inrolls': 0,  # TODO
    'Outrolls': 0,  # TODO
}

print(
   'Hand usage:',
   f' - Left hand: {keyboard.hand_usage_frequency(1):.2%}',
   f' - Right hand: {keyboard.hand_usage_frequency(2):.2%}',
   'Finger usage:',
   *(f' - Finger {finger.index}: {keyboard.finger_usage_percent(finger.index):.2%}' for finger in hands.fingers),
   'Row usage:',
   *(f' - Row {row}: {keyboard.row_usage_frequency(row):.2%}' for row in range(1, 5)),
   sep='\n'
)
