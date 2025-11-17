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


def resolve_corpus(corpus: str, raw: bool = False) -> pathlib.Path:
    """Resolve corpus folder path by name."""
    data_folder = pathlib.Path() / 'data'
    corpora = data_folder / 'corpora'

    if raw:
        return corpora / 'raw' / corpus
    return corpora / 'clean' / corpus


def resolve_keyboard(keyboard: str) -> pathlib.Path:
    """Resolve keyboard yaml file path by name."""
    data_folder = pathlib.Path() / 'data'
    keyboards = data_folder / 'keyboards'

    return keyboards / (keyboard + '.yaml')


def resolve_layout(layout: str) -> pathlib.Path:
    """Resolve layout yaml file path by name."""
    data_folder = pathlib.Path() / 'data'
    layouts = data_folder / 'layouts'

    return layouts / (layout + '.yaml')

def resolve_scan_folders(scan_folders: list[str]) -> list[pathlib.Path]:
    """Resolve list of scan folders making them type of path."""
    return [pathlib.Path(file) for file in scan_folders]

def resolve_content_output_path(content_output_path: str) -> pathlib.Path:
    """Resolve content output path txt file location."""
    data_folder = pathlib.Path() / 'data'
    corpora = data_folder / 'corpora'

    return corpora / 'raw' / (content_output_path + '.txt')

def setup(script_name=''):
    settings_folder = pathlib.Path() / 'settings'
    global_settings_path = settings_folder / 'settings.yaml'
    script_settings_path = settings_folder / f'{script_name}.yaml'

    script_settings = {}
    global_settings = {}

    global_settings: dict = yaml.safe_load(
        open(global_settings_path , encoding='utf-8')
    )

    if script_settings_path.is_file():
        script_settings: dict = yaml.safe_load(
            open(script_settings_path, encoding='utf-8')
        )

    ARGS = global_settings | script_settings
    ARGS.pop('aliases', None)
    ARGS.pop('anchors', None)

    # Parse arguments
    parser = argparse.ArgumentParser(prog=script_name)

    for argument in ARGS:
        add_argument(argument, parser, ARGS)

    ARGS.update(dict(parser.parse_args()._get_kwargs()))

    # Resolve paths
    is_raw = script_name == 'clean_cospus'
    is_scrapper = script_name == 'corpora_scrapper'

    ARGS['keyboard'] = resolve_keyboard(ARGS['keyboard'])
    ARGS['layout'] = resolve_layout(ARGS['layout'])
    ARGS['corpus'] = resolve_corpus(ARGS['corpus'], is_raw)

    if is_scrapper:
        ARGS['scan_folders'] = resolve_scan_folders(
            ARGS['scan_folders']
        )
        ARGS['content_output_path'] = resolve_content_output_path(
            ARGS['content_output_path']
        )

    # Display all settings
    from pprint import pprint
    pprint(ARGS)

    return ARGS
