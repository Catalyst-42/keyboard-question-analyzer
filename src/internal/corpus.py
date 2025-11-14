from __future__ import annotations

import pathlib
from collections import Counter


class Corpus():
    """Set of text used to calculate statistics.

    Used to calculate information about given
    set of text.
    """

    def __init__(self, name, text) -> None:
        """Created corpus from given text."""
        self.name = name
        self.text = text

        # Cached values
        self._usage: int | None = None 
        self._char_usage: Counter | None = None
        self._bigrams: Counter | None = None
        self._trigrams: Counter | None = None

    def prepare(self) -> None:
        """Calculate corpus stats."""
        # Full
        letters = self.text

        # Canonical
        # letters = ''.join(filter(lambda v: v.isalpha(), self.text))
        # letters = letters.lower()

        # Usage
        self._char_usage = Counter(letters)

        # Bigramms
        bigrams = (letters[i:i+2] for i in range(len(letters) - 1))
        self._bigrams = Counter(bigrams) 

        # Trigrams
        trigrams = (letters[i:i+3] for i in range(len(letters) - 2))
        self._trigrams = Counter(trigrams) 

    def _drop_cache(self) -> None:
        """Drops cached values."""
        self._usage = None
        self._char_usage = None
        self._bigrams = None
        self._trigrams = None

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

    @property
    def chars(self) -> str:
        """Return sorted string of corpus unique chars."""
        return ''.join(sorted(set(self.text)))

    @property
    def length(self) -> int:
        """Return length of all corpus content."""
        if self._usage is None:
            self.prepare()

        return self._usage

    @property
    def unigrams(self) -> Counter:
        """Returns dict of unigrams with usage."""
        if self.char_usage is None:
            self.prepare()

        return self._char_usage

    @property
    def bigrams(self) -> Counter:
        """Returns list of corpus bigrams."""
        if self._bigrams is None:
            self.prepare()

        return self._bigrams

    @property
    def trigrams(self) -> Counter:
        """Returns list of corpus trigrams."""
        if self._trigrams is None:
            self.prepare()

        return self._trigrams

    def clean(self, allowed_chars: str | list) -> None:
        """Filger current corpus text by filter string."""
        self.text = self.text.translate(
            str.maketrans('\t\n', '  ')
        )
        self.text = ''.join(
            [key for key in self.text if key in allowed_chars]
        )
        self._drop_cache()

    def limit(self, length) -> None:
        """Strip corpus content by given length."""
        self.text = self.text[:length]
        self._drop_cache()

    def char_usage(self, char: str) -> int:
        """Get character usage in corpus."""
        assert len(char) == 1, 'Char must be length of one'

        if self._char_usage is None:
            self.prepare()

        return self._char_usage.get(char, 0)
