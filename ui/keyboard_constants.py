BASE = 'BASE'
PREDICTED = 'PREDICTED'
NUMBERS = 'Numbers or Symbols'
ABC = 'A B C D E F G\nSpace'
HIJ = 'H I J K L M N\nBackspace'
OPQ = 'O P Q R S T U\nCaps'
VWX = 'V W X Y Z\n. ? !'
EXIT = 'Exit'
MAINMENU = 'Main Menu'
CLEAR = 'Clear'
CONFIRM = 'Confirm'
SPACE = 'Space'
BACKSPACE = 'Backspace'
CAPS = 'Toggle Caps'


TEXT_LAYOUTS = {
    0: [
        PREDICTED,
        PREDICTED,
        PREDICTED,
        NUMBERS,
        ABC,
        HIJ,
        OPQ,
        VWX
    ],
    1: [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        SPACE
    ],
    2: [
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        BACKSPACE
    ],
    3: [
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        CAPS
    ],
    4: [
        'V',
        'W',
        'X',
        'Y',
        'Z',
        '.',
        '?',
        '!'
    ]
}