from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_finger_usage')

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

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
    # TODO: ПЕРЕПИСАТЬ РУКИ НА ЛЕВУЮ И ПРАВУЮ И СЛОИ КЛАВИАТУРЫ НА W3C СТАНДАРТ
    'row_usage_top': keyboard.row_usage_frequency(2),
    'row_usage_home': keyboard.row_usage_frequency(3),
    'row_usage_bottom': keyboard.row_usage_frequency(4),
}

print(
   'Finger usage:',
   *(f' - Finger {finger.index}: {keyboard.finger_usage_frequency(finger.index):.2%}' for finger in hands.fingers),
   'Row usage:',
   *(f' - Row {row}: {keyboard.row_usage_frequency(row):.2%}' for row in range(1, 5)),
   sep='\n'
)
