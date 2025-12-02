import requests

import pathlib

from internal.corpus import Corpus
from internal.hands import Hands
from internal.keyboard import Keyboard
from internal.visualizer import Visualizer

def report(keyboard, corpora_names):
    """Calculate all metrics and prepare data for Django API."""
    visualizer_args = {
        'color_by': 'frequency',
        'combined_2': False,
        'layers': 1,
        'show_fingers': False,
        'show_frequencies': True,
        'show_home_keys': False,
        'show_key_codes': False,
        'show_keys_centers': False,
        'show_layout': True,
        'show_modifiers': True,
        'show_row_numbers': False,
        'smallcaps': True
    }

    hands = Hands(keyboard)

    # Get id's from database
    req = requests.get('http://localhost:8000/api/keyboards/', params={'search': keyboard.name})
    req: dict = req.json()[0]
    keyboard_id = req.get('id')

    req = requests.get('http://localhost:8000/api/layouts/', params={'search': keyboard.layout_name})
    req: dict = req.json()[0]
    layout_id = req.get('id')

    corpus_name = corpora_names[keyboard.corpus.name]
    req = requests.get('http://localhost:8000/api/corpora/', params={'search': corpus_name})
    req: dict = req.json()[0]
    corpus_id = req.get('id')

    # Generate frequency heatmap
    visualizer = Visualizer(keyboard, visualizer_args)
    visualizer.render(visualizer_args['layers'])
    heatmap_filename = f'{keyboard.layout_file}_{keyboard.file}_{corpus.name}.png'
    visualizer.savefig(heatmap_filename, dpi=300, transparent=True)
    visualizer.close()

    # Simulate typing for travel distance
    hands.simulate_typing(keyboard, corpus, False)

    # Prepare metrics data matching Django model
    report = {
        'corpus': corpus_id,
        'keyboard': keyboard_id,
        'layout': layout_id,

        # Travel distance metrics
        'travel_distance': hands.travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_1': hands.fingers[1].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_2': hands.fingers[2].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_3': hands.fingers[3].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_4': hands.fingers[4].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_5': hands.fingers[5].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_6': hands.fingers[6].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_7': hands.fingers[7].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_8': hands.fingers[8].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_9': hands.fingers[9].travel_distance / keyboard.one_unit / corpus.length,
        'travel_distance_finger_10': hands.fingers[10].travel_distance / keyboard.one_unit / corpus.length,

        # Finger usage (%)
        'finger_usage_1': keyboard.finger_usage_frequency(1),
        'finger_usage_2': keyboard.finger_usage_frequency(2),
        'finger_usage_3': keyboard.finger_usage_frequency(3),
        'finger_usage_4': keyboard.finger_usage_frequency(4),
        'finger_usage_5': keyboard.finger_usage_frequency(5),
        'finger_usage_6': keyboard.finger_usage_frequency(6),
        'finger_usage_7': keyboard.finger_usage_frequency(7),
        'finger_usage_8': keyboard.finger_usage_frequency(8),
        'finger_usage_9': keyboard.finger_usage_frequency(9),
        'finger_usage_10': keyboard.finger_usage_frequency(10),

        # Row usage (%)
        'row_usage_k': keyboard.row_usage_frequency('K'),
        'row_usage_e': keyboard.row_usage_frequency('E'),
        'row_usage_d': keyboard.row_usage_frequency('D'),
        'row_usage_c': keyboard.row_usage_frequency('C'),
        'row_usage_b': keyboard.row_usage_frequency('B'),
        'row_usage_a': keyboard.row_usage_frequency('A'),

        # Same Finger Bigrams (SFB)
        'same_finger_bigram_frequency': keyboard.same_finger_bigram_frequency,
        'same_finger_bigram_mean_distance': keyboard.same_finger_bigram_mean_distance,

        # Same Finger Skipgrams (SFS)
        'same_finger_skipgram_frequency': keyboard.same_finger_skipgram_frequency,
        'same_finger_skipgram_mean_distance': keyboard.same_finger_skipgram_mean_distance,

        # Scissors
        'half_scissor_bigram_frequency': keyboard.half_scissor_bigram_frequency,
        'full_scissor_bigram_frequency': keyboard.full_scissor_bigram_frequency,

        'half_scissor_skipgram_frequency': keyboard.half_scissor_skipgram_frequency,
        'full_scissor_skipgram_frequency': keyboard.full_scissor_skipgram_frequency,

        # Lateral Stretch Bigrams (LSB)
        'lateral_stretch_bigram_frequency': keyboard.lateral_stretch_bigram_frequency,
        'lateral_stretch_skipgram_frequency': keyboard.lateral_stretch_skipgram_frequency,

        # Trigrams
        'roll_frequency': keyboard.roll_frequency,
        'alternate_frequency': keyboard.alternate_frequency,
        'onehand_frequency': keyboard.onehand_frequency,
        'redirect_frequency': keyboard.redirect_frequency,
    }

    files = {
        'frequency_heatmap': open(heatmap_filename, 'rb'),
    }

    return report, files

def upsert(metrics, files):
    # Check if metric already exists
    req = requests.get('http://localhost:8000/api/metrics/', params={
        'corpus__id': metrics['corpus'],
        'keyboard__id': metrics['keyboard'],
        'layout__id': metrics['layout'],
    })

    # Not exists, create
    if len(req.json()) == 0:
        requests.post(
            'http://localhost:8000/api/metrics/',
            data=metrics,
            files=files
        )
        print('Status: created')
        return

    # Exists, update all but not images
    metric_id = req.json()[0]['id']
    requests.patch(
        f'http://localhost:8000/api/metrics/{metric_id}/',
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

corpora_paths = pathlib.Path() / 'data' / 'corpora' / 'clean'
corpora_paths = [*corpora_paths.glob('*')]

keyboard_paths = pathlib.Path() / 'data' / 'keyboards'
keyboard_paths = [*keyboard_paths.glob('*.yaml')]
keyboard_paths = [k for k in keyboard_paths if '_100' not in k.parts]

layout_paths = pathlib.Path() / 'data' / 'layouts'
layout_paths = layout_paths.glob('**/*.yaml')
layout_paths = [p for p in layout_paths if 'kq' not in p.parts]

combination = 1

for i, corpus_path in enumerate(corpora_paths):
    corpus = Corpus.load(corpus_path)

    for j, keyboard_path in enumerate(keyboard_paths):
        for k, layout_path in enumerate(layout_paths):
            if corpus_to_code[corpus.name] not in layout_path.parts:
                continue

            print(f'Combination {combination}')
            print(corpus.name, keyboard_path.name, layout_path.name)
            keyboard = Keyboard.load(keyboard_path, layout_path, corpus)

            process(keyboard, corpora_names)
            combination += 1
