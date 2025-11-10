# KeyboardQuestion
Analysis of keyboard effectivenes.

Stages of getting metrics:
- Create physical keyboard
  - Define physical keys, it's position on free canvas
- Create layout
  - Create mapping for physical keys
- Get bigramms list
  - Define corpus
  - Find large amount of test text
  - Calculate bigramms
- Compute metrics

### Data hierarchy
- Keyboard
  - Physical key
    - Key code
    - Key layout
      - Layer
        - Key mapping
        - Key usage

### Terms
##### Key
Means physical key code. Prefer to use key codes, described in [W3C](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode#constants_for_keycode_value)

##### Mapping
Representation of pressed key.
For example, basic `KeyS` pressed on standard qwerty layout will give the `s` mapping.
But on jcuken it will give the `ы` mapping. 

##### Layout
The joints between physical keys and it's mappings.

##### Keyboard
Describes the position of physical keys, it's physical parameters.

### Keyboard profile

Keyboard layout describes list of available
physical keys with their location and sizes on canvas.

```
Key rectangle specs:
 x.y---w-.
  |      |
  h      |
  '------'
```

### Layout
```
`~ 1! 2@ 3# 4$ 5% 6^ 7& 8* 9( 0) -_ =+
   qQ wW eE rR tT yY uU iI oO pP [{ ]} \|
   aA sS dD fF gG hH jJ kK lL ;: '"
   zZ xX cC vV bB nN mM ,< .> /?
```

```
` 1 2 3 4 5 6 7 8 9 0 - =
  q w e r t y u i o p [ ] \
  a s d f g h j k l ; '
  z x c v b n m , . /

~ ! @ # $ % ^ & * ( ) _ +
  Q W E R T Y U I O P { } |
  A S D F G H J K L : "
  Z X C V B N M < > ? 
```

### Keys by fingers
```
   _.-._                _.-._
 _|2|3|4|              |7|8|9|_
|1| | | |              | | | 10|
| | | | |  _        _  | | | | |
| '     |/5/        \6\|     ' |
|       / /          \ \       |
 \       /            \       /
  |     |              |     |

         Usage of fingers           Usage of rows

 ╭╴00.00%              00.00%╶╮       1 00.00%
 │ ╭╴00.00%          00.00%╶╮ │       2 00.00%
 1 2 3 4                7 8 9 10      3 00.00%
     │ ╰╴00.00%  00.00%╶╯ │           4 00.00%
     ╰╴00.00%      00.00%╶╯           5 00.00%

 Left - 00.00%    00.00% - Right
```

```
0 0 1 2 3 3 6 6 7 8 9 9 9
  0 1 2 3 3 6 6 7 8 9 9 9 9
  0 1 2 3 3 6 6 7 8 9 9
  0 1 2 3 3 6 6 7 8 9
```

### Which keys can move
Can be used if you want to lock some keys, locks should be created for
each layer of keyboard layout

```
1 1 1 1 1 1 1 1 1 1 1 1 1
  1 1 1 1 1 1 1 1 1 1 1 1 1
  1 1 1 1 1 1 1 1 1 1 1
  1 1 1 1 1 1 1 1 1 1
```

# Database

- Corpus
  - Name (s)
  - Number of unique symbols (n)
  - Size (n)
  - Bigramms (f)

- Keyboard
  - Name (s)
  - Form factor (s)
  - Keys (n)
  - Rows (n)
  - Keyboard model (yaml)

- Layout
  - Name (s)
  - Language (s)
  - Layout model (yaml)

- Metric
  - Corpus (f)
  - Keyboard (f)
  - Layout (f)
  - Travel dictance (n)
    - Total (n)
    - Finger 1 (n)
    - Finger 2 (n)
    - Finger 3 (n)
    - Finger 4 (n)
    - Finger 5 (n)
    - Finger 6 (n)
    - Finger 7 (n)
    - Finger 8 (n)
    - Finger 9 (n)
    - Finger 10 (n)
  - Hand usage (%)
    - Left hand (%)
    - Right hand (%)
  - Finger usage (%)
    - Finger 1 (%)
    - Finger 2 (%)
    - Finger 3 (%)
    - Finger 4 (%)
    - Finger 5 (%)
    - Finger 6 (%)
    - Finger 7 (%)
    - Finger 8 (%)
    - Finger 9 (%)
    - Finger 10 (%)
  - Row usage (%)
    - Row 1 (%)
    - Row 2 top (%)
    - Row 3 home (%)
    - Row 4 bottom (%)
    - Row 5 (%)
    - ...
  - Scissors (%)
    - Left hand (%)
    - Right hand (%)
  - Same finger bigrams (%)
    - Left hand (%)
    - Right hand (%)
  - Alternating finger bigrams (%)
    - Left hand (%)
    - Right hand (%)
  - Rolling (%)
    - Inrolls (%)
    - Outrolls (%)
  - Redirects [triads]
    - Left hand (%)
    - Right hand (%)

- Frequency
  - Corpus (f)
  - Key (s)
  - Entrances (n)

- Bigramm
  - Corpus (id)
  - Pair (s)
  - Entrances (n)

# Web application

- Main
  - Total keyboards
  - Total layouts
  - Total corpuses
- Desctiption of metrics
  - All in one page?
- List of layouts
  - All information in list (order by key?)
    - Compact view or giant table with sorters
  - Comparsion in table
- Layout page
  - All info from metrics
  - Images of layout
  - Images of frequency
  - Maps for metrics, ae graph for finger usage
- Additional info about
  - Corpuses
  - Keyboards
  - Bigrams

# Images

- Images
  - Layout
    - preview
    - freqency

  - Keyboard
    - debug
