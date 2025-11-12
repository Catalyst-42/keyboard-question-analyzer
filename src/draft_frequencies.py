import yaml

from internal.keyboard import Keyboard
from internal.setup import setup
from internal.corpus import Corpus

ARGS = setup("frequencies")
collector = Corpus(ARGS["corpus"])

# Compute frequency
frequencies = {}

if ARGS["only_layout_mappings"]:
    keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])
    keys = keyboard.chars
else:
    keys = collector.chars()

for key in keys:
    frequencies[key] = collector._char_usage(key)

# Output result
frequencies = dict(sorted(frequencies.items(), key=lambda v: -v[1]))
data = {"info": "Frequency stats", "frequencies": frequencies}
print(yaml.dump(data, indent=2, allow_unicode=True, sort_keys=False))
