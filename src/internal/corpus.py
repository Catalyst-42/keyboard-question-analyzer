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
            print(f'Error: corpus {path} is not found!')
            exit()

        for file in files_to_process:
            with open(file, encoding='utf-8', errors='ignore') as file:
                text += file.read()

        return Corpus(name, text)

    @property
    def unique_keys(self):
        return ''.join(sorted(set(self.text)))

    @property
    def size(self):
        return len(self.text)

    def key_occurances(self, key):
        return self.text.count(key)
