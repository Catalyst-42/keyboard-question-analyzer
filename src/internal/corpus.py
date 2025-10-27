import pathlib

class Corpus():
    def __init__(self, corpus_text):
        self.corpus_text = corpus_text

    @classmethod 
    def load(self, corpus_folder):
        corpus_text = ""
        files_to_process = set()

        # Gather all text from source directory
        path = pathlib.Path(corpus_folder)

        if path.is_dir():
            files_to_process.update(path.glob("**/*"))
        else:
            print(f"Error: corpus {corpus_folder} is not found!")
            exit()

        for file in files_to_process:
            with open(file, encoding="utf-8", errors="ignore") as file:
                corpus_text += file.read()

        return Corpus(corpus_text)

    def get_unique_keys(self):
        return set(self.corpus_text)

    def count_key_occuraence(self, key):
        return self.corpus_text.count(key)
