from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_travel_distance')

keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], ARGS['frequency'])
corpus = Corpus.load(ARGS['corpus'])
hands = Hands(keyboard)

for i, char in enumerate(corpus.text):
    key = keyboard.key_for(char)

    if not key:
        continue

    hands.move_to(key.finger, key)
    print(f'\rProgress: {i/len(corpus.text):.2%} ', end='')

else:
    print('\n')  # Get rid of empty end stat output

print(
    'Travel distance:',
    ' - Left hand:',
    *(f'  - {i}: {int(hands.fingers[i].travel_distance)}' for i in range(1, 5 + 1)),
    ' - Right hand:',
    *(f'  - {i}: {int(hands.fingers[i].travel_distance)}' for i in range(6, 10 + 1)),
    '\nTotal:',
    f' - Left hand: {int(hands.get_left_hand_travel_distance())}',
    f' - Right hand: {int(hands.get_right_hand_travel_distance())}',
    f' - Both: {int(hands.get_total_travel_distance())}',
    sep='\n'
)
