from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.setup import setup
from internal.visualizer import Visualizer

ARGS = setup('layout_display')

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)

# Show keyboard layout
visualizer = Visualizer(keyboard, ARGS)
visualizer.render(ARGS['layers'])
filename = f'{keyboard.layout_file}_{keyboard.file}.png'
visualizer.savefig(filename, dpi=300, transparent=True)

visualizer.show()
