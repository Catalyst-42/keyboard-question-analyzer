from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_ngramms')

corpus = Corpus.load(ARGS['corpus'])
# corpus = Corpus('custom', 'burn')
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

print(keyboard.info(), '\n')

report = {
    '%_same_finger_bigram_frequcency': keyboard.same_finger_bigram_frequency,
    'u_same_finger_bigram_mean_distance': keyboard.same_finger_bigram_mean_distance,
    '%_half_scissor_bigram_frequency': keyboard.half_scissor_bigram_frequency,
    '%_full_scissor_bigram_frequency': keyboard.full_scissor_bigram_frequency,
    '%_same_finger_skipgram_frequency': keyboard.same_finger_skipgram_frequency,
    'u_same_finger_skipgram_mean_distance': keyboard.same_finger_skipgram_mean_distance,
    '%_half_scissor_skipgram_frequency': keyboard.half_scissor_skipgram_frequency,
    '%_full_scissor_skipgram_frequency': keyboard.full_scissor_skipgram_frequency,
    '%_lateral_stretch_bigram_frequency': keyboard.lateral_stretch_bigram_frequency,
    '%_lateral_stretch_skipgram_frequency': keyboard.lateral_stretch_skipgram_frequency,
    '%_roll_frequency': keyboard.roll_frequency,
    '%_alternate_frequency': keyboard.alternate_frequency,
    'f_roll:alternation': keyboard.roll_frequency / keyboard.alternate_frequency,
    '%_onehand_frequency': keyboard.onehand_frequency,
    '%_redirect_frequency': keyboard.redirect_frequency,
}

for feature in report:
    name = feature
    prefix = feature[0]
    feature = feature[2:]

    if prefix == '%':
        print(f'{feature}: {report[name]:.2%}')
    elif prefix == 'u':
        print(f'{feature}: {report[name]:.3}u')
    elif prefix == 'f':
        print(f'{feature}: {report[name]:.2}')
