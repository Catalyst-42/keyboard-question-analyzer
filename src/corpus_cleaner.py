import pathlib

from internal.corpus import Corpus
from internal.setup import *

ARGS = setup('corpus_cleaner')
corpus = Corpus.load(ARGS['corpus'])

length_before = corpus.length
chars_before = corpus.chars

corpus.clean(ARGS['allowed_keys'])
corpus.limit(ARGS['limit_keys'])

length_after = corpus.length
chars_after = corpus.chars

# Save
file_path: pathlib.Path = (
    ARGS['corpus'].parent.parent
    / 'clean'
    / f'{corpus.name}'
    / f'{corpus.name}.txt'
)
file_path.parent.mkdir(parents=True, exist_ok=True)

with open(file_path, 'w') as file:
    file.write(corpus.text)

print(
    f'Cleaned {corpus.name} corpus',
    '\nWas:',
    f' - {length_before:,} chars',
    f' - {len(chars_before)} unique keys',
    '\nNow:',
    f' - {length_after:,} chars',
    f' - {len(chars_after)} unique keys',
    sep='\n'
)
