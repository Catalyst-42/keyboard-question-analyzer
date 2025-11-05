import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.patheffects as pe
from matplotlib import colormaps

from internal.keyboard import Keyboard
from internal.setup import setup

class Visualizer():
    def __init__(self, keyboard, config):
        self.keyboard = keyboard
        self.config = config

        self.axs = None
        self.fig = None

        self.bboxes = {}

    def display(self, number_of_layers):
        layers = [[f'layer{i}'] for i in range(1, number_of_layers + 1)]

        self.fig, self.axs = plt.subplot_mosaic(
            layers,
            figsize=(8, 3 * number_of_layers)
        )
        self.fig.canvas.manager.set_window_title("Keyboard")

        # Render each layer
        for layer in range(1, number_of_layers + 1):
            self.draw_keyboard(layer)
            self.set_format_coord(layer)
            self.set_styles(layer)
            self.set_aspect_ratio(layer)

        self.show()

    def _get_key_color(self, layer, key):
        if self.config["color_by"] in "frequency":
            return colormaps["Purples"](
                (key.get_usage(layer) / self.keyboard.get_max_usage()) ** 0.3
            )

        if self.config["color_by"] in "row":
            return colormaps["Pastel1"](key.row - 1)

        if self.config["color_by"] in "finger":
            return colormaps["Set3"](key.finger - 1)

        if self.config["color_by"] in "hand":
            return colormaps["Set3"](key.finger > 5)

        return (0, 0, 0, 0)

    def _draw_key_patch(self, key, patch_color):
        return ptc.FancyBboxPatch(
            (key.x, -key.y - key.h),
            key.w,
            key.h,
            boxstyle="round,rounding_size=3",
            linewidth=1,
            facecolor=patch_color,
            edgecolor="black",
        )

    def _draw_key_layout(self, layer, key):
        self.axs[f"layer{layer}"].text(
            key.x + key.w/2,
            -key.y - key.h/2 + 0.5,
            key.get_mapping(layer),
            color="white",
            path_effects=[
                pe.withStroke(linewidth=2, foreground="black")
            ],
            va="center_baseline",
            ha="center",
            fontsize=14
        )

    def _draw_key_code(self, layer, key):
        self.axs[f"layer{layer}"].text(
            key.x + key.w/2,
            -key.y - key.h/2 + 0.5,
            key.key,
            color="white",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")],
            va="top",
            ha="center",
            fontsize=7
        )

    def _draw_key_home_icon(self, layer, key):
        self.axs[f"layer{layer}"].text(
            key.x + key.w - 1.5,
            -key.y - 0.5,
            "•",
            color="white",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")],
            va="top",
            ha="right",
            fontsize=6
        )

    def _draw_key_freqency(self, layer, key):
        self.axs[f"layer{layer}"].text(
            key.x + key.w/2,
            -key.y - key.h + 0.5,
            f"{key.get_frequency(layer):.2%}",
            color="white",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")],
            va="bottom",
            ha="center",
            fontsize=6
        )

    def draw_keyboard(self, layer):
        keyboard_bbox = [0, 0, 0, 0]

        for key in self.keyboard.keys:
            if not self.config["show_modifiers"] and key.is_modifier:
                continue

            patch_color = self._get_key_color(layer, key)
            key_patch = self._draw_key_patch(key, patch_color)

            # Extend view box to contain all patches
            x0, y0, x1, y1 = key_patch.get_bbox().extents
            keyboard_bbox[0] = min(keyboard_bbox[0], x0)
            keyboard_bbox[1] = min(keyboard_bbox[1], y0)
            keyboard_bbox[2] = max(keyboard_bbox[2], x1)
            keyboard_bbox[3] = max(keyboard_bbox[3], y1)

            self.bboxes[layer] = keyboard_bbox
            self.axs[f"layer{layer}"].add_patch(key_patch)

            # Display key info
            if self.config["show_layout"]:
                self._draw_key_layout(layer, key)

            if self.config["show_key_codes"]:
                self._draw_key_code(layer, key)

            if self.config["show_row_numbers"] or self.config["show_fingers"]:
                row_or_finger = ""
                if self.config["show_row_numbers"]:
                    row_or_finger += f"r{key.row}"

                if self.config["show_fingers"]:
                    row_or_finger += f"f{key.finger}"

                self.axs[f"layer{layer}"].text(
                    key.x + 1.5,
                    -key.y - 1.5,
                    row_or_finger,
                    color="white",
                    path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                    va="top",
                    ha="left",
                    fontsize=6
                )

            if key.is_home and self.config["show_home_keys"]:
                self._draw_key_home_icon(layer, key)

            if self.config["show_frequencies"]:
                self._draw_key_freqency(layer, key)

    def set_format_coord(self, layer):
        def format_coord(x, y):
            selected_key = None

            # Get current key
            for key in keyboard.keys:
                if (key.x <= x <= key.x + key.w) and (key.y <= -y <= key.y + key.h):
                    selected_key = key
                    break

            if not selected_key:
                return ""

            return (
                f"{key.key} \"{key.get_mapping(layer)}\", finger {key.finger}, row {key.row}\n"
                f"Frequency: {key.get_frequency(layer):.2%} on mapping, total: {key.get_total_frequency():.2%} (x, y) = ({key.x}, {key.y})"
            )

        self.axs[f"layer{layer}"].format_coord = format_coord

    def set_styles(self, layer):
        keyboard_padding = 1
        keyboard_bbox = self.bboxes[layer]

        limits = {
            'x_min': keyboard_bbox[0] - keyboard_padding,
            'x_max': keyboard_bbox[2] + keyboard_padding,
            'y_min': keyboard_bbox[1] - keyboard_padding,
            'y_max': keyboard_bbox[3] + keyboard_padding,
        }

        # Limit view in bbox
        self.axs[f"layer{layer}"].set_xlim(limits['x_min'], limits['x_max'])
        self.axs[f"layer{layer}"].set_ylim(limits['y_min'], limits['y_max'])

    def set_aspect_ratio(self, layer):
        self.axs[f"layer{layer}"].axis("off")
        self.axs[f"layer{layer}"].set_aspect("equal")

    def show(self):
        plt.tight_layout()
        plt.show()

# Show stats data
ARGS = setup("display")

keyboard = Keyboard.load(
    ARGS["keyboard"],
    ARGS["layout"],
    ARGS["frequency"]
)
keyboard.print_keyboard_usage()

visualizer = Visualizer(keyboard, ARGS)
visualizer.display(2)
