import pandas as pd
import numpy as np
from collections import Counter
import os
import yaml

from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

ARGS = setup("display")

collector = Corpus.load(ARGS["corpus"])
text = collector.text

bigrams = [text[i:i+2] for i in range(len(text)-1)]
bigram_counts = Counter(bigrams)

result = []
for bigram, count in bigram_counts.items():
    result.append({'bigram': bigram, 'count': count})

df = pd.DataFrame(result)
df = df.sort_values('count', ascending=False)
df = df[~df['bigram'].str.contains(r'[ \t\n]', na=False)]

output_data = {}
for _, row in df.iterrows():
    bigram_key = row['bigram'] # .replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
    output_data[bigram_key] = int(row['count'])

os.makedirs('./data/bigramms', exist_ok=True)
corpus_name = os.path.basename(ARGS["corpus"]).replace('.', '_')
filename = f'./data/bigramms/{corpus_name}.yaml'

with open(filename, 'w', encoding='utf-8') as f:
    yaml.dump(output_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print('done')