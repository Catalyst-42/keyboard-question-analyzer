import yaml

from setup import setup

ARGS = setup("frequency-checker")

# Gather all text from source files
corpus_text = ""
for file_path in ARGS["files"]:
    with open(file_path, encoding="utf-8", errors="ignore") as file:
        corpus_text += file.read()

# Compute keys frequency
frequencies = {}

keys = ARGS["allowed_glyphs"] if ARGS["allowed_glyphs"] else set(corpus_text)
keys = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"

for key in keys:
    frequencies[key] = corpus_text.count(key)

# Output result
frequencies = dict(sorted(frequencies.items(), key=lambda v: -v[1]))
data = {"frequencies": frequencies}
print(yaml.dump(data, indent=2, allow_unicode=True))
