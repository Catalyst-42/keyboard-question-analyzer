import argparse
import pathlib

import yaml


def add_argument(argument: str, parser: argparse.ArgumentParser, ARGS: dict):
    match argument:
        # Global
        case "keyboard":
            parser.add_argument(
                "--keyboard",
                help=(
                    "File which contain information about. File must be placed in data/keyboards folder"
                    " keyboard keys placement"
                ),
                default=ARGS["keyboard"],
                type=str,
                dest="keyboard",
            )

        case "layout":
            parser.add_argument(
                "--layout",
                help=(
                    "File which contain information about keyboard. File must be placed in data/layouts folder"
                    " language layout of keys"
                ),
                default=ARGS["layout"],
                type=str,
                dest="layout",
            )

        case "frequency":
            parser.add_argument(
                "--frequency",
                help="File which contain information about key usage frequency. File must be placed in data/frequencies folder",
                default=ARGS["frequency"],
                type=str,
                dest="frequency",
            )

        # Display
        case "show_modifiers":
            parser.add_argument(
                "-m",
                help="Display modifier keys",
                action="store_const",
                const=not ARGS["show_modifiers"],
                default=ARGS["show_modifiers"],
                dest="show_modifiers",
            )

        case "show_layout":
            parser.add_argument(
                "-l",
                help="Draw layout mappings on keys at the center",
                action="store_const",
                const=not ARGS["show_layout"],
                default=ARGS["show_layout"],
                dest="show_layout",
            )

        case "show_key_codes":
            parser.add_argument(
                "-k",
                help="Draw key codes mappings on keys at the top",
                action="store_const",
                const=not ARGS["show_key_codes"],
                default=ARGS["show_key_codes"],
                dest="show_key_codes",
            )
        case "show_rows":
            parser.add_argument(
                "-r",
                help=(
                    "Draw number of row mapping for"
                    " the keys at the top right position",
                ),
                action="store_const",
                const=not ARGS["show_rows"],
                default=ARGS["show_rows"],
                dest="show_rows",
            )

        case "show_fingers":
            parser.add_argument(
                "-f",
                help="Draw finger mapping on keys at the top left position",
                action="store_const",
                const=not ARGS["show_fingers"],
                default=ARGS["show_fingers"],
                dest="show_fingers",
            )

        case "show_frequencies":
            parser.add_argument(
                "-p",
                help="Draw layout key usage frequencies",
                action="store_const",
                const=not ARGS["show_frequencies"],
                default=ARGS["show_frequencies"],
                dest="show_frequencies",
            )

        case "show_home_keys":
            parser.add_argument(
                "-hk",
                help="Display dots on top right corner of home keys",
                action="store_const",
                const=not ARGS["show_home_keys"],
                default=ARGS["show_home_keys"],
                dest="show_home_keys",
            )

        case "show_row_numbers":
            parser.add_argument(
                "-r",
                help="",
                action="store_const",
                const=not ARGS["show_row_numbers"],
                default=ARGS["show_row_numbers"],
                dest="show_row_numbers",
            )

        case "color_by":
            parser.add_argument(
                "-c",
                help=(
                    "Mark key background according to data of frequency,"
                    "row, hand, finger or none"
                ),
                type=str,
                default=ARGS["color_by"],
                dest="color_by",
            )

        case "corpus":
            parser.add_argument(
                "--corpus",
                help="Directory for corpus of text for keyboard efficency analysis",
                default=ARGS["corpus"],
                type=str,
            )


def setup(script_name=''):
    settings_folder = pathlib.Path() / 'settings'
    global_settings_path = settings_folder / 'settings.yaml'
    script_settings_path = settings_folder / f'{script_name}.yaml'

    script_settings = {}
    global_settings = {}

    global_settings: dict = yaml.safe_load(
        open(global_settings_path , encoding='utf-8')
    )

    if script_settings_path.is_file:
        script_settings: dict = yaml.safe_load(
            open(script_settings_path, encoding='utf-8')
        )

    ARGS = global_settings | script_settings
    ARGS.pop('aliases', None)

    # Parse arguments
    parser = argparse.ArgumentParser(prog=script_name)

    for argument in ARGS:
        add_argument(argument, parser, ARGS)

    ARGS.update(dict(parser.parse_args()._get_kwargs()))

    # Full paths for global settings
    data_folder = pathlib.Path() / 'data'

    keyboards = data_folder / 'keyboards'
    layouts = data_folder / 'layouts'
    frequencies = data_folder / 'frequencies'
    corpora = data_folder / 'corpora'

    ARGS['keyboard'] = keyboards / f'{ARGS['keyboard']}.yaml'
    ARGS['layout'] = layouts / f'{ARGS['layout']}.yaml'
    ARGS['frequency'] = frequencies / f'{ARGS['frequency']}.yaml'

    if script_name == 'corpus_cleaner':
        ARGS['corpus'] = corpora / 'raw' / ARGS['corpus']
    else:
        ARGS['corpus'] = corpora / 'clean' / ARGS['corpus']

    if script_name == 'corpora_scrapper':
        ARGS['scan_folders'] = [pathlib.Path(file) for file in ARGS['scan_folders']]
        ARGS['content_output_path'] = corpora / 'raw' / f'{ARGS['content_output_path']}.txt'

    # from pprint import pprint
    # pprint(ARGS)
    return ARGS
