from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup("display")

keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])
collector = Corpus.load(ARGS["corpus"])

hands = Hands()
hands.goto_homerow(keyboard)

travel_distance = 0

import pandas as pd

def get_bigram_frequencies(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_series = pd.Series(bigrams)
    freq_table = bigram_series.value_counts()
    return freq_table

text = collector.corpus_text
bigram_freq = get_bigram_frequencies(text)
print(bigram_freq)

# for i, key in enumerate(collector.corpus_text):
#     physical_key = keyboard.key_for(key)

#     if physical_key:
#         travel_distance += hands.goto(physical_key.finger, physical_key)

#     print(f"\rProgress: {i/len(collector.corpus_text):.2%} ", end="")

# else:
#     print()  # Get rid of empty end stat output

# print(f"Total travel distance: {int(travel_distance):,}")
