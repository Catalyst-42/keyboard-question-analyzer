import pathlib

import yaml

from keyboard import Keyboard
from setup import setup

ARGS = setup("frequencies")

# Gather all text from source files
corpus_text = ""
files_to_process = set()

for file_path in ARGS["file_paths"]:
    path = pathlib.Path(file_path)

    if path.is_file():
        files_to_process.add(path)

    if path.is_dir():
        files_to_process.update(path.glob("**/*"))

for file_path in files_to_process:
    with open(file_path, encoding="utf-8", errors="ignore") as file:
        corpus_text += file.read()

# Compute frequency
frequencies = {}

if ARGS["only_layout_mappings"]:
    keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])
    keys = keyboard.mappings
else:
    keys = set(corpus_text)

for key in keys:
    frequencies[key] = corpus_text.count(key)

# Output result
frequencies = dict(sorted(frequencies.items(), key=lambda v: -v[1]))
data = {"info": "Frequency stats", "frequencies": frequencies}
print(yaml.dump(data, indent=2, allow_unicode=True, sort_keys=False))
