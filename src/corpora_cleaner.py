import pathlib

from internal.corpus import Corpus
from internal.setup import *

ARGS = setup('corpora_cleaner')
corpus = Corpus.load(ARGS['corpus'])

# Filter text and limit
clean_text = corpus.text.translate(
    str.maketrans('\t\n', '  ')
)
clean_text = ''.join(
    [key for key in clean_text if key in ARGS['allowed_keys']]
)

if ARGS['limit_keys']:
    clean_text = clean_text[:ARGS['limit_keys']]

# Save
file_path: pathlib.Path = (
    ARGS['corpus'].parent.parent / 'clean' /
    f'{corpus.name}' / f'{corpus.name}.txt'
)
file_path.parent.mkdir(parents=True, exist_ok=True)

with open(file_path, 'w') as file:
    file.write(clean_text)

print(
    f'Cleaned {corpus.name} corpus',
    '\nWas:',
    f' - {corpus.size:,} chars',
    f' - {len(corpus.unique_keys)} unique keys',
    '\nNow:',
    f' - {len(clean_text):,} chars',
    f' - {len(set(clean_text))} unique keys',
    sep='\n'
)
