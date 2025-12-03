from __future__ import annotations

import pathlib
from collections import Counter
from functools import cached_property

from yaml import safe_load

class Corpus():
    """Set of text used to calculate statistics.

    Used to calculate information about given
    set of text.
    """

    def __init__(self, name, text):
        """Created corpus from given text."""
        self.name = name
        self.text = text

    def _drop_cache(self):
        """Drops cached values. If a field doesn't exist, it's skipped."""
        for attr in ('length', 'unigrams', 'bigrams', 'trigrams'):
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    @classmethod 
    def load(self, corpus_folder) -> Corpus:
        """Load corpus from given folder and name it after it."""
        text = ''
        files_to_process = set()

        # Gather all text from source directory
        path = pathlib.Path(corpus_folder)
        name = path.name

        if path.is_dir():
            files_to_process.update(path.glob('**/*'))
        else:
            raise FileNotFoundError(f'Corpus on path {path} is not found')

        for file in files_to_process:
            with open(file, encoding='utf-8', errors='ignore') as file:
                text += file.read()

        return Corpus(name, text)

    @classmethod
    def load_mockup(self, unigram_frequency_path):
        """Load mockup corpus with frequency by separate file."""
        unigrams: dict = safe_load(
            open(unigram_frequency_path, encoding="utf-8").read()
        )

        corpus = Corpus('Mockup', '')

        # Replace unigrams on mockup ones
        corpus.unigrams = unigrams['frequencies']
        return corpus

    @property
    def chars(self) -> str:
        """Return sorted string of corpus unique chars."""
        return ''.join(sorted(set(self.text)))

    @cached_property
    def length(self) -> int:
        """Return length of all corpus content."""
        return len(self.text)

    @cached_property
    def unigrams(self) -> Counter:
        """Returns counter dict of corpus unigrams."""
        unigrams = Counter(self.text)
        return unigrams

    @cached_property
    def bigrams(self) -> Counter:
        """Returns counter dict of corpus bigrams."""
        groups = (self.text[i:i+2] for i in range(len(self.text) - 1))
        bigrams = Counter(groups) 

        return bigrams

    @cached_property
    def trigrams(self) -> Counter:
        """Returns counter dict of corpus trigrams."""
        groups = (self.text[i:i+3] for i in range(len(self.text) - 2))
        trigrams = Counter(groups) 

        return trigrams

    def clean(self, allowed_chars: str | set = None, filter_func: callable = None):
        """Filger corpus text by given chars or function."""
        if allowed_chars:
            self.text = ''.join(
                [key for key in self.text if key in allowed_chars]
            )

        if filter_func:
            self.text = ''.join(
                filter(filter_func, self.text)
            )

        self._drop_cache()

    def limit(self, length):
        """Strip corpus content by given length."""
        self.text = self.text[:length]
        self._drop_cache()

    def char_usage(self, char: str) -> int:
        """Get character usage in corpus."""
        return self.unigrams.get(char, 0)
