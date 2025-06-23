import matplotlib.pyplot as plt
import numpy as np

ru_initial_data = [('о', 258652, 'ru'), ('а', 182852, 'ru'), ('е', 177340, 'ru'), ('т', 158866, 'ru'), ('н', 138023, 'ru'), ('и', 136133, 'ru'), ('с', 109021, 'ru'), ('л', 98504, 'ru'), ('р', 90044, 'ru'), ('в', 83150, 'ru'), ('д', 71435, 'ru'), ('м', 71114, 'ru'), ('к', 69913, 'ru'), ('п', 60146, 'ru'), ('у', 56621, 'ru'), ('.', 50808, 'pn'), ('я', 49469, 'ru'), (',', 48811, 'pn'), ('ь', 48381, 'ru'), ('ы', 41558, 'ru'), ('ч', 40850, 'ru'), ('б', 38460, 'ru'), ('з', 31868, 'ru'), ('г', 31616, 'ru'), ('й', 23580, 'ru'), ('ж', 20337, 'ru'), ('-', 19948, 'pn'), ('х', 18194, 'ru'), ('ш', 16768, 'ru'), ('ё', 14338, 'ru'), ('ю', 13690, 'ru'), ('[', 12097, 'pn'), (']', 12095, 'pn'), ('э', 11523, 'ru'), ('щ', 8701, 'ru'), ('Н', 7519, 'ru'), ('ц', 6073, 'ru'), ('ф', 5416, 'ru'), ('П', 5343, 'ru'), ('В', 5061, 'ru'), ('И', 4143, 'ru'), ('С', 3496, 'ru'), ('?', 3082, 'pn'), ('А', 3079, 'ru'), ('Т', 2882, 'ru'), ('Д', 2797, 'ru'), ('К', 2698, 'ru'), ('О', 2528, 'ru'), ('0', 2476, 'nu'), ('Я', 2460, 'ru'), (':', 2303, 'pn'), ('М', 2290, 'ru'), ('1', 2157, 'nu'), ('2', 2040, 'nu'), ('"', 1974, 'pn'), ('(', 1935, 'pn'), (')', 1930, 'pn'), ('!', 1701, 'pn'), ('Э', 1575, 'ru'), ('Р', 1565, 'ru'), ('З', 1369, 'ru'), ('3', 1273, 'nu'), ('Х', 1227, 'ru'), ('Б', 1165, 'ru'), ('Ч', 1119, 'ru'), ('4', 1072, 'nu'), ('5', 989, 'nu'), ('У', 933, 'ru'), ('Л', 930, 'ru'), ('Е', 817, 'ru'), ('Г', 779, 'ru'), ('6', 734, 'nu'), ('8', 716, 'nu'), ('9', 710, 'nu'), ('7', 654, 'nu'), ('/', 632, 'pn'), ('=', 506, 'pn'), ('ъ', 362, 'ru'), ('%', 312, 'pn'), ('Ф', 300, 'ru'), ('+', 235, 'pn'), ('_', 232, 'pn'), ('Ж', 186, 'ru'), ('Ш', 128, 'ru'), (';', 114, 'pn'), ('Ц', 74, 'ru'), ('Ю', 28, 'ru'), ('Й', 11, 'ru'), ('Ы', 6, 'ru'), ('Щ', 6, 'ru'), ('Ё', 5, 'ru'), ('№', 3, 'un')]


eng_initial_data = [('e', 5303, 'en'), ('n', 4478, 'en'), ('t', 4208, 'en'), ('o', 3959, 'en'), ('a', 3801, 'en'), ('i', 3476, 'en'), ('r', 2902, 'en'), ('s', 2757, 'en'), ('p', 2757, 'en'), ('S', 2727, 'en'), ('g', 2162, 'en'), ('l', 1936, 'en'), ('d', 1558, 'en'), ('m', 1409, 'en'), ('c', 1401, 'en'), ('u', 1363, 'en'), ('h', 1080, 'en'), ('b', 1051, 'en'), ('G', 1047, 'en'), ('P', 1046, 'en'), ('y', 905, 'en'), ('T', 904, 'en'), ('f', 835, 'en'), ('R', 799, 'en'), ('O', 697, 'en'), ('v', 623, 'en'), ('k', 580, 'en'), ('x', 567, 'en'), ('C', 535, 'en'), ('w', 530, 'en'), ('A', 507, 'en'), ('E', 482, 'en'), ('D', 461, 'en'), ('N', 443, 'en'), ('L', 423, 'en'), ('M', 415, 'en'), ('Y', 322, 'en'), ('B', 320, 'en'), ('F', 305, 'en'), ('W', 291, 'en'), ('I', 270, 'en'), ('H', 265, 'en'), ('U', 263, 'en'), ('V', 229, 'en'), ('J', 218, 'en'), ('j', 204, 'en'), ('q', 136, 'en'), ('K', 113, 'en'), ('z', 74, 'en'), ('Z', 65, 'en'), ('Q', 51, 'en'), ('X', 48, 'en')]

ru_data = {}
eng_data = {}

for i in ru_initial_data:
    ru_data[i[0]] = i[1]

for i in eng_initial_data:
    eng_data[i[0]] = i[1]


# keyboard = [
#     "]1234567890-=  ",
#     " йцукенгшщзхъё ",
#     " фывапролджэ   ",
#     " ячсмитьбю/    ",
# ]

# shift_keyboard = [
#     "[!\"№%:,.;()_+ ",
#     " ЙЦУКЕНГШЩЗХЪЁ ",
#     " ФЫВАПРОЛДЖЭ   ",
#     " ЯЧСМИТЬБЮ?    ",
# ]

keyboard = [
    "*◦§▪ъё?!-­—)«„‘ ",
    " цья,.звкдчшщ  ",
    " уиеоалнтсрй   ",
    " фэхыюбмпгж    ",
]

shift_keyboard = [
    "*◦§▪ЪЁ?!-­—)«„‘ ",
    " ЦЬЯ,.ЗВКДЧШЩ  ",
    " УИЕОАЛНТСРЙ   ",
    " ФЭХЫЮБМПГЖ    ",
]

print("Russian keys (base and shift): " + ''.join(keyboard).replace(' ', '') + ''.join(shift_keyboard).replace(' ', ''))

qwerty = [
    "`1234567890-=   ",
    "vxnpqukbcz[]\   ",
    "hitemados;'     ",
    "gylfjwr,./      "
]

shift_qwerty = [
    "~!@#$%^&*()_+   ",
    " QWERTYUIOP{}|  ",
    " ASDFGHJKL:\"   ",
    " ZXCVBNM<>?     "
]

print("English keys (base and shift): " + ''.join(qwerty).replace(' ', '') + ''.join(shift_qwerty).replace(' ', ''))

fig, axs = plt.subplot_mosaic(
    [
        ["Basic", "QWERTY"],
        ["Shift", "Shift QWERTY"],
    ],
    figsize=(13.5, 5.7),
)

fig.canvas.manager.set_window_title("Тепловая карта ЙЦУКЕН и QWERTY")

ax = list(axs.items())
ax[0][1].set_axis_off()
ax[2][1].set_axis_off()

ax[1][1].set_axis_off()
ax[3][1].set_axis_off()

popularity = np.zeros((4, 14))
shift_popularity = np.zeros((4, 14))

qwerty_popularity = np.zeros((4, 14))
shift_qwerty_popularity = np.zeros((4, 14))

for i, line in enumerate(keyboard):
    for j, key in enumerate(line):
        if key not in ru_data:
            continue

        popularity[i, j] = ru_data[key]

for i, line in enumerate(shift_keyboard):
    for j, key in enumerate(line):
        if key not in ru_data:
            continue

        shift_popularity[i, j] = ru_data[key]

for i, line in enumerate(qwerty):
    for j, key in enumerate(line):
        if key not in eng_data:
            continue

        qwerty_popularity[i, j] = eng_data[key]

for i, line in enumerate(shift_qwerty):
    for j, key in enumerate(line):
        if key not in eng_data:
            continue

        shift_qwerty_popularity[i, j] = eng_data[key]

# Annotate
for i in range(4):
    for j in range(14):
        text = ax[0][1].text(j, i, keyboard[i][j], ha="center", va="center")
        text = ax[2][1].text(j, i, shift_keyboard[i][j], ha="center", va="center")
        
        text = ax[1][1].text(j, i, qwerty[i][j], ha="center", va="center")
        text = ax[3][1].text(j, i, shift_qwerty[i][j], ha="center", va="center")

im = ax[0][1].imshow(popularity, cmap='Reds', vmax=max(np.max(popularity), np.max(shift_popularity)))
im = ax[2][1].imshow(shift_popularity, cmap='Reds', vmax=max(np.max(popularity), np.max(shift_popularity)))

eng_max = max(np.max(qwerty_popularity), np.max(shift_qwerty_popularity))

im = ax[1][1].imshow(qwerty_popularity, cmap='Reds', vmax=eng_max)
im = ax[3][1].imshow(shift_qwerty_popularity, cmap='Reds', vmax=eng_max)

ax[0][1].set_title("Основной ЙЦУКЕН", loc='left')
ax[2][1].set_title("Shift ЙЦУКЕН", loc='left')

ax[1][1].set_title("Основной QWERTY", loc='left')
ax[3][1].set_title("Shift QWERTY", loc='left')

ax[0][1].grid(which="minor", color="w", linestyle='-', linewidth=3)
ax[2][1].grid(which="minor", color="w", linestyle='-', linewidth=3)
ax[1][1].grid(which="minor", color="w", linestyle='-', linewidth=3)
ax[3][1].grid(which="minor", color="w", linestyle='-', linewidth=3)

fig.tight_layout()
plt.show()
