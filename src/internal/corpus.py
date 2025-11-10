import pathlib


class Corpus():
    def __init__(self, name, text):
        self.name = name
        self.text = text

    @classmethod 
    def load(self, corpus_folder):
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
        return ''.join(sorted(set(self.text)))

    @property
    def length(self) -> int:
        return len(self.text)

    def clean(self, filter_string):
        self.text = self.text.translate(
            str.maketrans('\t\n', '  ')
        )
        self.text = ''.join(
            [key for key in self.text if key in filter_string]
        )

    def limit(self, length):
        self.text = self.text[:length]

    def char_usage(self, char: str) -> int:
        return self.text.count(char)

