from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup("display")

keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])
collector = Corpus.load(ARGS["corpus"])

print(
    collector.unique_keys(),
    collector.size()
)

hands = Hands()
hands.goto_homerow(keyboard)

travel_distance = 0
for i, key in enumerate(collector.text):
    physical_key = keyboard.key_for(key)

    if physical_key:
        travel_distance += hands.goto(physical_key.finger, physical_key)

    print(f"\rProgress: {i/len(collector.text):.2%} ", end="")

else:
    print()  # Get rid of empty end stat output

print(f"Total travel distance: {int(travel_distance):,}")
