from internal.keyboard import Keyboard
from internal.setup import setup
from internal.visualizer import Visualizer

ARGS = setup('display')

# Constraint for combiner
if ARGS['combined_2']:
    ARGS['layers'] = 1

# Load keyboard
keyboard = Keyboard.load(
    ARGS['keyboard'],
    ARGS['layout'],
    ARGS['frequency']
)
keyboard.print_keyboard_usage()

# Show keyboard layout
visualizer = Visualizer(keyboard, ARGS)
visualizer.render(ARGS['layers'])

# visualizer.savefig('keyboard.png', dpi=300)
visualizer.show()
