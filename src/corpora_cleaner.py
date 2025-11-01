import pathlib

from internal.corpus import Corpus
from internal.setup import *

ARGS = setup('clean_corpus')
corpus = Corpus.load(ARGS['corpus'])

ALLOWED_KEYS = '!"%()+,-./0123456789:;=?[]_ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяё№ '
LIMIT_KEYS = 10_000_000 

# Filter text and limit
clean_text = corpus.text.translate(
    str.maketrans('\t\n', '  ')
)
clean_text = ''.join(
    [key for key in clean_text if key in ALLOWED_KEYS]
)

if LIMIT_KEYS:
    clean_text = clean_text[:LIMIT_KEYS]

# Save
file_path: pathlib.Path = (
    ARGS['corpus'].parent.parent / 'clean' /
    f'{corpus.name}' / f'{corpus.name}.txt'
)
file_path.parent.mkdir(parents=True, exist_ok=True)

with open(file_path, 'w') as file:
    file.write(clean_text)

print(
    f'Cleaned {corpus.name} corpus\n'
    f'\nWas:\n'
    f' - {corpus.size:,} chars\n'
    f' - {len(corpus.unique_keys)} unique keys\n'
    f'\nNow:\n'
    f' - {len(clean_text):,} chars\n'
    f' - {len(set(clean_text))} unique keys'
)
