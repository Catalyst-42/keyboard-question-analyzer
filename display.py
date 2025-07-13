import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.patheffects as pe
from matplotlib import colormaps

from keyboard import Keyboard
from setup import setup

ARGS = setup("display")
keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequencies"])


def draw_keyboard(layer: int, keyboard: Keyboard):
    keyboard_padding = 1
    keyboard_bbox = [0, 0, 0, 0]

    for key in keyboard.keys:
        if not ARGS["show_modifiers"] and key.is_modifier:
            continue

        # Choice colormap for key
        if ARGS["color_by"].lower() in "frequency":
            patch_color = colormaps["Purples"]((key.get_usage(layer) / keyboard.get_max_usage()) ** 0.3)
        elif ARGS["color_by"].lower() in "row":
            patch_color = colormaps["Pastel1"](key.row - 1)
        elif ARGS["color_by"].lower() in "finger":
            patch_color = colormaps["Set3"](key.finger - 1)
        elif ARGS["color_by"].lower() in "hand":
            patch_color = colormaps["Set3"](key.finger > 5)
        else:
            patch_color = (0, 0, 0, 0)

        key_patch = ptc.FancyBboxPatch(
            (key.x, -key.y - key.h),
            key.w,
            key.h,
            boxstyle="round,rounding_size=3",
            linewidth=1,
            facecolor=patch_color,
            edgecolor="black",
        )

        # Find all patch canvas border
        x0, y0, x1, y1 = key_patch.get_bbox().extents
        keyboard_bbox[0] = min(keyboard_bbox[0], x0)
        keyboard_bbox[1] = min(keyboard_bbox[1], y0)
        keyboard_bbox[2] = max(keyboard_bbox[2], x1)
        keyboard_bbox[3] = max(keyboard_bbox[3], y1)

        axs[f"layer{layer}"].add_patch(key_patch)

        # Display key info
        if ARGS["show_layout"]:
            axs[f"layer{layer}"].text(
                key.x + key.w/2,
                -key.y - key.h/2 + 0.5,
                key.get_mapping(layer),
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="center_baseline",
                ha="center",
                fontsize=14
            )

        if ARGS["show_key_codes"]:
            axs[f"layer{layer}"].text(
                key.x + key.w/2,
                -key.y - key.h/2 + 0.5,
                key.key,
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="top",
                ha="center",
                fontsize=7
            )

        if ARGS["show_rows"] or ARGS["show_fingers"]:
            row_or_finger = ""
            if ARGS["show_rows"]:
                row_or_finger += f"r{key.row}"

            if ARGS["show_fingers"]:
                row_or_finger += f"f{key.finger}"

            axs[f"layer{layer}"].text(
                key.x + 1.5,
                -key.y - 1.5,
                row_or_finger,
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="top",
                ha="left",
                fontsize=6
            )

        if key.is_home and ARGS["show_home_keys"]:
            axs[f"layer{layer}"].text(
                key.x + key.w - 1.5,
                -key.y - 0.5,
                "•",
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="top",
                ha="right",
                fontsize=6
            )

        if ARGS["show_frequencies"] and not key.is_modifier:
            axs[f"layer{layer}"].text(
                key.x + key.w/2,
                -key.y - key.h + 0.5,
                f"{key.get_frequency(layer):.2%}",
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="bottom",
                ha="center",
                fontsize=6
            )

    def format_coord(x, y):
        selected_key = None
        for key in keyboard.keys:
            if (key.x <= x <= key.x + key.w) and (key.y <= -y <= key.y + key.h):
                selected_key = key
                break

        if not selected_key:
            return ""

        return (
            f"{key.key} \"{key.get_mapping(layer)}\", finger {key.finger}, row {key.row}\n"
            f"Frequency: {key.get_frequency(layer):.2%} on mapping, total: {key.get_total_frequency():.2%}"
        )

    axs[f"layer{layer}"].format_coord = format_coord
    axs[f"layer{layer}"].set_xlim(keyboard_bbox[0] - keyboard_padding, keyboard_bbox[2] + keyboard_padding)
    axs[f"layer{layer}"].set_ylim(keyboard_bbox[1] - keyboard_padding, keyboard_bbox[3] + keyboard_padding)

    axs[f"layer{layer}"].axis("off")
    axs[f"layer{layer}"].set_aspect("equal")


# Show stats data
keyboard.print_keyboard_usage()

# Generate plot
fig, axs = plt.subplot_mosaic(
    [["layer1"],
     ["layer2"]],
    figsize=(8, 6)
)

fig.canvas.manager.set_window_title("Keyboard")

draw_keyboard(1, keyboard)
draw_keyboard(2, keyboard)

plt.tight_layout()
plt.show()
