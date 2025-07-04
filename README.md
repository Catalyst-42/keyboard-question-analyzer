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

### Keyboard profile

Keyboard layout describes list of available
physical keys with their location and sizes on canvas.

Key rectangle specs:
 x.y---w-.
  |      |
  h      |
  '------'

```
` 1 2 3 4 5 6 7 8 9 0 - =   
0 0 1 2 3 3 6 6 7 8 9 9 9
1 1 1 1 1 1 1 1 1 1 1 1 1

  q w e r t y u i o p [ ] \ 
  0 1 2 3 3 6 6 7 8 9 9 9 9
  1 1 1 1 1 1 1 1 1 1 1 1 1

  a s d f g h j k l ; '     
  0 1 2 3 3 6 6 7 8 9 9
  1 1 1 1 1 1 1 1 1 1 1

  z x c v b n m , . /       
  0 1 2 3 3 6 6 7 8 9
  1 1 1 1 1 1 1 1 1 1
```

But, how about... distance?

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
   _.-._           _.-._
 _|1|2|3|         |6|7|8|_
|0| | | |         | | | |9|
| | | | |  _   _  | | | | |
| '     |/4/   \5\|     ' |
|       / /     \ \       |
 \       /       \       /
  |     |         |     |
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
