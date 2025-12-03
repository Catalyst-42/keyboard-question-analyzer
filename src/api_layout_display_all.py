"""
Used to fill backend API with layout previews.
Calculates all previews for all combinations
of keyboards and layouts.
"""

import pathlib

import requests

from internal.corpus import Corpus
from internal.keyboard import Keyboard
from internal.visualizer import Visualizer


def report(keyboard, corpora_names):
    """Calculate all metrics and prepare data for Django API."""
    visualizer_args = {
        'color_by': 'home',
        'combined_2': True,
        'layers': 1,
        'show_fingers': False,
        'show_frequencies': False,
        'show_home_keys': True,
        'show_key_codes': False,
        'show_keys_centers': False,
        'show_layout': True,
        'show_modifiers': True,
        'show_row_numbers': False,
        'smallcaps': False
    }

    # Get id's from database
    req = requests.get('http://localhost:8000/api/keyboards/', params={'search': keyboard.name})
    req: dict = req.json()[0]
    keyboard_id = req.get('id')

    req = requests.get('http://localhost:8000/api/layouts/', params={'search': keyboard.layout_name})
    req: dict = req.json()[0]
    layout_id = req.get('id')

    # Generate frequency heatmap
    visualizer = Visualizer(keyboard, visualizer_args)
    visualizer.render(visualizer_args['layers'])

    layout_preview_filename = f'{keyboard.layout_file}_{keyboard.file}.png'
    visualizer.savefig(layout_preview_filename, dpi=300, transparent=True)
    visualizer.close()

    # Prepare metrics data matching Django model
    report = {
        'keyboard': keyboard_id,
        'layout': layout_id,
    }

    files = {
        'layout_preview': open(layout_preview_filename, 'rb'),
    }

    return report, files

def upsert(metrics, files):
    # Check if metric already exists
    req = requests.get('http://localhost:8000/api/layout-previews/', params={
        'keyboard__id': metrics['keyboard'],
        'layout__id': metrics['layout'],
    })

    # Not exists, create
    if len(req.json()) == 0:
        requests.post(
            'http://localhost:8000/api/layout-previews/',
            data=metrics,
            files=files
        )
        print('Status: created')
        return

    # Exists, update all but not images
    preview_id = req.json()[0]['id']
    requests.patch(
        f'http://localhost:8000/api/layout-previews/{preview_id}/',
        data=metrics,
        # files=files
    )
    print('Status: updated')


def process(keyboard, corpora_names):
    metrics, files = report(keyboard, corpora_names)
    upsert(metrics, files)
    print()

    # Display
    # for field in metrics:
    #     print(f'{field}: {metrics[field]}')

corpus_to_code = {
    'english': 'en',
    'code': 'en',
    'russian': 'ru',
    'diaries': 'ru',
}

corpora_names = {
    'english': 'Английский',
    'russian': 'Русский',
    'code': 'Код',
    'diaries': 'Дневники',
}

keyboard_paths = pathlib.Path() / 'data' / 'keyboards'
keyboard_paths = [*keyboard_paths.glob('*.yaml')]

layout_paths = pathlib.Path() / 'data' / 'layouts'
layout_paths = layout_paths.glob('**/*.yaml')
layout_paths = [p for p in layout_paths if 'kq' not in p.parts]

combination = 1

for j, keyboard_path in enumerate(keyboard_paths):
    for k, layout_path in enumerate(layout_paths):
        print(f'Combination {combination}')
        print(keyboard_path.name, layout_path.name)
        keyboard = Keyboard.load(keyboard_path, layout_path, Corpus('Empty', ''))

        process(keyboard, corpora_names)
        combination += 1
