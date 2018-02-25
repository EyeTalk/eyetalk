BASE = 'BASE'
PREDICTED = 'NO PREDICTED WORD'
NUMBERS = 'Numbers\nand\nSymbols'
ABC = 'A B C D\nE F G\nSpace'
HIJ = 'H I J K \nL M N\nDelete'
OPQ = 'O P Q R\nS T U\nCaps'
VWX = 'V W X Y\nZ . ? !'
EXIT = 'EXIT'
BACK = 'BACK'
MAINMENU = 'MAIN MENU'
CLEAR = 'CLEAR'
CONFIRM = 'CONFIRM'
SPACE = 'SPACE'
BACKSPACE = 'BACKSPACE'
CAPS = 'TOGGLE CAPS'


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