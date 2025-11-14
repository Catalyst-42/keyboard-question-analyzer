from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_ngramms')

keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], ARGS['corpus'])
corpus = Corpus('custom', 'Hello world')
# corpus = Corpus.load(ARGS['corpus'])
hands = Hands(keyboard)

print(corpus.bigrams)
print(corpus.trigrams)

total_bigrams = 0
total_trigrams = 0

print('Tri:', corpus.bigrams.total(), corpus.length)
print('Bri:', corpus.trigrams.total(), corpus.length)
