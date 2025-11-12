from __future__ import annotations

import pathlib


class Corpus():
    """Set of text used to calculate statistics.

    Used to calculate information about given
    set of text.
    """

    def __init__(self, name, text):
        """Init corpus."""
        self.name = name
        self.text = text

        # Cached values
        self._usage: int | None = None 
        self._char_usage: dict[str, int] | None = None

    def prepare(self):
        """Calculate corpus stats."""
        self._char_usage = {}
        for char in self.chars:
            self._char_usage[char] = self.text.count(char)

        assert len(self.text) == sum(self._char_usage.values())
        self._usage = len(self.text)

    def _drop_cache(self):
        """Drops cached values."""
        self._usage = None
        self._char_usage = None

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

    def clean(self, filter_string):
        """Removes all chars by filter string in corpus."""
        self.text = self.text.translate(
            str.maketrans('\t\n', '  ')
        )
        self.text = ''.join(
            [key for key in self.text if key in filter_string]
        )
        self._drop_cache()

    def limit(self, length):
        """Strip corpus content by given length."""
        self.text = self.text[:length]
        self._drop_cache()

    def char_usage(self, char: str) -> int:
        """Calculate character usage."""
        assert len(char) == 1, 'Char must be length of one'

        if self._char_usage is None:
            self.prepare()

        return self._char_usage.get(char, 0)
