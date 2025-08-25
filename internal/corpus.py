import pathlib

class Corpus():
    def __init__(self, corpus_text):
        self.corpus_text = corpus_text

    @classmethod 
    def load(self, corpus):
        corpus_text = ""
        files_to_process = set()

        # Gather all text from source directory
        path = pathlib.Path(corpus)

        if path.is_dir():
            files_to_process.update(path.glob("**/*"))
        else:
            print(f"Error: corpus {corpus} is not found!")
            exit()

        for corpus in files_to_process:
            with open(corpus, encoding="utf-8", errors="ignore") as file:
                corpus_text += file.read()

        return Corpus(corpus_text)

    def get_unique_keys(self):
        return set(self.corpus_text)

    def count_key_occuraence(self, key):
        return self.corpus_text.count(key)
