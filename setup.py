import argparse
import tomllib


def add_argument(argument: str, parser: argparse.ArgumentParser, ARGS: dict):
    match argument:
        case "help":
            parser.add_argument(
                "-help",
                action="help",
                default=argparse.SUPPRESS,
                help="Show all script startup parameters and exit"
            )

        # Global
        case "frequencies":
            parser.add_argument(
                "-frequencies",
                help=(
                    "File which contain information about key usage frequency",
                ),
                default=ARGS["frequencies"],
                type=str,
                dest="frequencies",
            )

        case "keyboard":
            parser.add_argument(
                "-keyboard",
                help=(
                    "File which contain information about"
                    " keyboard keys placement",
                ),
                default=ARGS["keyboard"],
                type=str,
                dest="keyboard",
            )

        case "layout":
            parser.add_argument(
                "-layout",
                help=(
                    "File which contain information about keyboard"
                    " language layout of keys",
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
                "-h",
                help="Display dots on top right corner of home keys",
                action="store_const",
                const=not ARGS["show_home_keys"],
                default=ARGS["show_home_keys"],
                dest="show_home_keys",
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

        case "files":
            parser.add_argument(
                "files",
                help="List of files to be processed",
                default=ARGS["files"],
                type=str,
                nargs='+'
            )


def setup(script_name):
    settings = tomllib.load(open("settings.toml", "rb"))
    ARGS = settings[script_name]

    options = {}
    if "options" in ARGS:
        options = ARGS.pop("options")
        ARGS |= options

    # Parse arguments
    parser = argparse.ArgumentParser(add_help=False)
    add_argument("help", parser, ARGS)

    for argument in ARGS:
        add_argument(argument, parser, ARGS)

    parsed_args = dict(parser.parse_args()._get_kwargs())
    for arg in parsed_args:
        ARGS[arg] = parsed_args[arg]

    # print(ARGS)
    return ARGS
