from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_travel_distance')

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

print(keyboard.info(), '\n')

for i, char in enumerate(corpus.text):
    key = keyboard.key_by_mapping(char)

    if not key:
        continue

    hands.move_to(key.finger, key)
    print(f'\rProgress: {i/len(corpus.text):.2%} ', end='')

else:
    print('\n')  # Get rid of empty end stat output

td = hands.travel_distance
td_left_hand = hands.travel_distance_left_hand
td_right_hand = hands.travel_distance_right_hand

# Assets obvious things
td_eq_hands = td == td_left_hand + td_right_hand,
td_eq_fingers = td == sum(finger.travel_distance for finger in hands.fingers),

assert td_eq_hands, "Hand td don't coverage with total"
assert td_eq_fingers, "Finger td don't coverage"

# print(
#     'Travel distance:',
#     ' - Left hand:',
#     *(f'  - {finger.index}: {int(finger.travel_distance)}' for finger in hands.fingers[:5]),
#     ' - Right hand:',
#     *(f'  - {finger.index}: {int(finger.travel_distance)}' for finger in hands.fingers[5:]),
#     '\nTotal:',
#     f' - Left hand: {int(td_left_hand)}',
#     f' - Right hand: {int(td_right_hand)}',
#     f' - Both: {int(td)}',
#     sep='\n'
# )



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