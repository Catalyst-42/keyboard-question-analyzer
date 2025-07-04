import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.patheffects as pe
from matplotlib import colormaps

import json

physical_layout: dict = json.load(open("data/physical_layouts/ansi_60.json"))
logical_layout: dict = json.load(open("data/logical_layouts/jcuken.json"))
keys_frequencies: dict = json.load(open("data/keys_frequencies/russian.json"))

total_keys_pressed = sum(keys_frequencies.values())
colormap = colormaps["Purples"]

HIDE_CONTROL_KEYS = False

def get_mapping(physical_key, layout: dict, layer: int):
    if physical_key in layout["Controls"]:
        return layout["Controls"][physical_key]["Icon"]
    
    elif physical_key in layout["Mappings"]:
        return layout["Mappings"][physical_key][str(layer)]
    
    else:
        return ""

def create_keyboard_heatmap(layer: int, keyboard: dict, layout: dict):
    keyboard_padding = 1
    keyboard_bbox = [0, 0, 0, 0]

    for physical_key in keyboard:
        is_control_key = False
        if physical_key["Key"] in layout["Controls"]:
            is_control_key = True
            if HIDE_CONTROL_KEYS:
                continue

        key_mapping = get_mapping(physical_key["Key"], layout, layer)
        key_usage_frequency = keys_frequencies.get(key_mapping, 0) / max(keys_frequencies.values())
        
        patch_color = colormap(key_usage_frequency ** 0.3)
        patch_color = colormaps["Pastel1"](int(physical_key["Row"]) - 1)
        
        key_patch = ptc.FancyBboxPatch(
            (physical_key["X"], -physical_key["Y"] - physical_key["H"]),
            physical_key["W"],
            physical_key["H"],
            boxstyle="round,rounding_size=3",
            linewidth=1,
            facecolor=patch_color,
            edgecolor="black",
        )

        x0, y0, x1, y1 = key_patch.get_bbox().extents
        keyboard_bbox[0] = min(keyboard_bbox[0], x0)
        keyboard_bbox[1] = min(keyboard_bbox[1], y0)
        keyboard_bbox[2] = max(keyboard_bbox[2], x1)
        keyboard_bbox[3] = max(keyboard_bbox[3], y1)

        axs[f"layer{layer}"].add_patch(key_patch)
        axs[f"layer{layer}"].text(
            physical_key["X"] + physical_key["W"]/2,
            -physical_key["Y"] - physical_key["H"]/2 + 0.5,
            key_mapping,
            color="white",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")],
            va="center_baseline",
            ha="center",
            fontsize=14
        )
        
        if not is_control_key:
            axs[f"layer{layer}"].text(
                physical_key["X"] + physical_key["W"]/2,
                -physical_key["Y"] - physical_key["H"] + 0.5,
                f"{keys_frequencies.get(key_mapping, 0) / sum(keys_frequencies.values()):.2%}",
                color="white",
                path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                va="bottom",
                ha="center",
                fontsize=6
            )

    axs[f"layer{layer}"].set_xlim(keyboard_bbox[0] - keyboard_padding, keyboard_bbox[2] + keyboard_padding)
    axs[f"layer{layer}"].set_ylim(keyboard_bbox[1] - keyboard_padding, keyboard_bbox[3] + keyboard_padding)

    axs[f"layer{layer}"].axis("off")
    axs[f"layer{layer}"].set_aspect("equal")
    
# Generate heatmaps
fig, axs = plt.subplot_mosaic(
    [["layer1"],
    ["layer2"]],
    figsize=(8, 6)
)

fig.canvas.manager.set_window_title("Keyboard")

create_keyboard_heatmap(1, physical_layout, logical_layout)
create_keyboard_heatmap(2, physical_layout, logical_layout)

plt.tight_layout()
plt.show()
