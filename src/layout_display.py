from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.setup import setup
from internal.visualizer import Visualizer

ARGS = setup('layout_display')

# Constraint for combiner
if ARGS['combined_2']:
    ARGS['show_layout'] = False 
    ARGS['layers'] = 1

corpus = Corpus.load(ARGS['corpus'])
keyboard = Keyboard.load(ARGS['keyboard'], ARGS['layout'], corpus)

# Show keyboard layout
visualizer = Visualizer(keyboard, ARGS)
visualizer.render(ARGS['layers'])
visualizer.savefig('layout.png', dpi=300, transparent=True)
visualizer.show()
