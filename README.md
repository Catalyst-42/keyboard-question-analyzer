# KeyboardQuestion
Analysis of keyboard effectivenes.

Stages of editing:
- Create physical keyboard
  - Define physical keys, it's position on free canvas
- Create layout
  - Create mapping for physical keys
  - Also test it with input
- Watch statistics
  - From frequency file color layout

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
But on jcucken it will give the `ы` mapping. 

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
