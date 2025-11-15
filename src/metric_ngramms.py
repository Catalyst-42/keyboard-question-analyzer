from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup('metric_ngramms')

corpus = Corpus.load(ARGS['corpus'])
# corpus = Corpus('custom', '')
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)
hands = Hands(keyboard)

print(keyboard.info(), '\n')

report = {
    '%_sfb_frequcency': keyboard.sfb_frequency,
    'u_sfb_mean_distance': keyboard.sfb_mean_distance,
    '%_sfs_frequency': keyboard.sfs_frequency,
    '%_fsb_frequency': keyboard.fsb_frequency,
}

for feature in report:
    name = feature
    prefix = feature[0]
    feature = feature[2:]

    if prefix == '%':
        print(f'{feature}: {report[name]:.2%}')
    elif prefix == 'u':
        print(f'{feature}: {report[name]:.3}u')
    elif prefix == 'i':
        print(f'{feature}: {round(report[name]):.2}')
