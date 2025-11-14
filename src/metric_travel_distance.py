from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_travel_distance')

keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], ARGS['corpus'])
corpus = Corpus.load(ARGS['corpus'])
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

report = {
    
}

print(
    'Travel distance:',
    ' - Left hand:',
    *(f'  - {finger.index}: {int(finger.travel_distance)}' for finger in hands.fingers[:5]),
    ' - Right hand:',
    *(f'  - {finger.index}: {int(finger.travel_distance)}' for finger in hands.fingers[5:]),
    '\nTotal:',
    f' - Left hand: {int(td_left_hand)}',
    f' - Right hand: {int(td_right_hand)}',
    f' - Both: {int(td)}',
    sep='\n'
)
