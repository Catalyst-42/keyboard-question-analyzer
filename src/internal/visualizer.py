import matplotlib.patches as ptc
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from internal.keyboard import Key, Keyboard
from internal.rounded_polygon import RoundedPolygon


class Visualizer():
    def __init__(self, keyboard: Keyboard, config: dict):
        self.keyboard = keyboard
        self.config = config

        self.axs: dict[str, Axes]
        self.fig: Figure

        self.bboxes = {}

    def render(self, number_of_layers: int):
        layers = [[f'layer{i}'] for i in range(1, number_of_layers + 1)]

        self.fig, self.axs = plt.subplot_mosaic(
            layers,
            figsize=(8, 3 * number_of_layers)
        )

        # Render each layer
        for layer in range(1, number_of_layers + 1):
            self.draw_keyboard(layer)
            self.set_format_coord(layer)
            self.set_styles(layer)
            self.set_layout(layer)

    def _get_key_color(self, layer: int, key: Key):
        if key.get_mapping(layer) == '∅':
            return 'red'

        if self.config['color_by'] in 'frequency':
            return colormaps['Purples'](
                (key.get_usage(layer) / self.keyboard.get_max_usage()) ** 0.5
            )

        if self.config['color_by'] in 'row':
            return colormaps['Pastel1'](key.row - 1)

        if self.config['color_by'] in 'finger':
            return colormaps['Set3'](key.finger - 1)

        if self.config['color_by'] in 'hand':
            return colormaps['Set3'](key.finger > 5)

        if self.config['color_by'] in 'home':
            return colormaps['Set3'](key.is_home + 2)

        return (0, 0, 0, 0)

    def _draw_key_patch(self, key: Key, patch_color):
        if key.notch:
            return self._draw_return_key_patch(key, patch_color)

        return ptc.FancyBboxPatch(
            (key.x, -key.y - key.h),
            key.w,
            key.h,
            boxstyle='round,rounding_size=3',
            linewidth=1,
            facecolor=patch_color,
            edgecolor='black',
        )

    def _draw_return_key_patch(self, key: Key, patch_color):
        # Notch place is bottom left
        xy = [
            (key.x + key.notch_w, -key.y - key.h),
            (key.x + key.w, -key.y - key.h),
            (key.x + key.w, -key.y),
            (key.x, -key.y),
            (key.x, -key.y - key.notch_h),
            (key.x + key.notch_w , -key.y - key.notch_h)
        ]

        return RoundedPolygon(
            xy=xy,
            pad=2.75,
            facecolor=patch_color,
            edgecolor='black',
            linewidth=1
        )

    def _draw_key_layout(self, layer: int, key: Key, upper=False):
        mapping = key.get_mapping(layer)

        if upper and len(mapping) == 1:
            mapping = mapping.upper()

        self.axs[f'layer{layer}'].text(
            *key.center(),
            mapping,
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='center_baseline',
            ha='center',
            fontsize=14
        )

    def _draw_key_layout_combined(self, layer: int, key: Key):
        if key.is_modifier or key.get_mapping(layer).upper() == key.get_mapping(layer + 1):
            self._draw_key_layout(layer, key, True)
            return

        # First layer
        self.axs[f'layer{layer}'].text(
            key.x + key.w * 2/4,
            -key.y - key.h * 3/4 + 0.5,
            key.get_mapping(layer),
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='center_baseline',
            ha='center',
            fontsize=12
        )

        # Second layer
        self.axs[f'layer{layer}'].text(
            key.x + key.w * 2/4,
            -key.y - key.h * 1/4 + 0.5,
            key.get_mapping(layer + 1),
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='center_baseline',
            ha='center',
            fontsize=12
        )

    def _draw_key_code(self, layer: int, key: Key):
        self.axs[f'layer{layer}'].text(
            *key.center(),
            key.key,
            rotation=28 if key.h <= 15 or (len(key.key) > 8 and key.w <= 40) else 0,
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='center',
            ha='center',
            fontsize=7
        )

    def _draw_key_home_icon(self, layer: int, key: Key):
        self.axs[f'layer{layer}'].text(
            key.x + key.w - 1.5,
            -key.y - 0.5,
            '•',
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='top',
            ha='right',
            fontsize=6
        )

    def _draw_key_freqency(self, layer: int, key: Key):
        if key.get_frequency(layer) == 0:
            return

        frequency = key.get_frequency(layer) 

        # Account second layer
        if self.config['combined_2']:
           frequency += key.get_frequency(layer + 1)

        self.axs[f'layer{layer}'].text(
            key.x + key.w/2,
            -key.y - key.h + 0.5,
            f'{frequency:.2%}',
            color='white',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
            va='bottom',
            ha='center',
            fontsize=6
        )

    def draw_keyboard(self, layer: int):
        keyboard_bbox = [0, 0, 0, 0]

        for key in self.keyboard.keys:
            if not self.config['show_modifiers'] and key.is_modifier:
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
            self.axs[f'layer{layer}'].add_patch(key_patch)

            # Display key info
            if self.config['show_layout']:
                self._draw_key_layout(layer, key)

            if self.config['combined_2']:
                self._draw_key_layout_combined(layer, key)

            if self.config['show_key_codes']:
                self._draw_key_code(layer, key)

            # Combine row and finger info
            row_and_finger = ''

            if self.config['show_row_numbers']:
                row_and_finger += f'r{key.row}'

            if self.config['show_fingers']:
                row_and_finger += f'f{key.finger}'

            if row_and_finger:
                self.axs[f'layer{layer}'].text(
                    key.x + 1.5,
                    -key.y - 1.5,
                    row_and_finger,
                    color='white',
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')],
                    va='top',
                    ha='left',
                    fontsize=6
                )

            if key.is_home and self.config['show_home_keys']:
                self._draw_key_home_icon(layer, key)

            if self.config['show_frequencies']:
                self._draw_key_freqency(layer, key)

    def set_format_coord(self, layer: int):
        def format_coord(x, y):
            # Get current key by cords
            for key in self.keyboard.keys:
                in_key_x = key.x <= x <= key.x + key.w
                in_key_y = key.y <= -y <= key.y + key.h

                if in_key_x and in_key_y:
                    key = key
                    break

            if not key:
                return ''

            mapping = key.get_mapping(layer)
            finger = key.finger
            row = key.row
            frequency = key.get_frequency(layer)
            total_frequency = key.get_total_frequency()

            return (
                f'{key.key} "{mapping}", finger {finger}, row {row} '
                f'frequency: {frequency:.2%} on mapping, '
                f'total: {total_frequency:.2%}\n'
                f'(x, y) = ({key.x}, {key.y})'
            )

        self.axs[f'layer{layer}'].format_coord = format_coord

    def set_styles(self, layer: int):
        keyboard_padding = 1
        keyboard_bbox = self.bboxes[layer]

        limits = {
            'x_min': keyboard_bbox[0] - keyboard_padding,
            'x_max': keyboard_bbox[2] + keyboard_padding,
            'y_min': keyboard_bbox[1] - keyboard_padding,
            'y_max': keyboard_bbox[3] + keyboard_padding,
        }

        # Limit view in bbox
        self.axs[f'layer{layer}'].set_xlim(limits['x_min'], limits['x_max'])
        self.axs[f'layer{layer}'].set_ylim(limits['y_min'], limits['y_max'])

    def set_layout(self, layer: int):
        self.fig.canvas.manager.set_window_title('Keyboard')

        self.axs[f'layer{layer}'].axis('off')
        self.axs[f'layer{layer}'].set_aspect('equal')

        plt.tight_layout()

    def show(self):
        plt.show()

    def savefig(self, name: str, *args, **kwargs):
        plt.savefig(name, *args, **kwargs)
