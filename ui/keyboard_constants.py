BASE = 'BASE'
PREDICTED = 'NO\nPREDICTED\nWORD'
NUMBERS = 'Numbers\nand\nSymbols'
ABC = 'A B C D\nE F G\nSpace'
HIJ = 'H I J K \nL M N\nBackspace'
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
YES = 'YES'
NO = 'NO'
OUTSIDE = 'OUTSIDE'
HOME = 'HOME'


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
    ],
    5: [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        'MORE->'
    ],
    6: [
        '<-BACK',
        '7',
        '8',
        '9',
        '#',
        '$',
        '%',
        '@'
    ]
}

GREETINGS = [
    "Hello,\nhow are you?",
    "Good to\nsee you",
    "Good\nmorning",
    "Good\nafternoon",
    "Goodnight",
    "Goodbye",
    "I'm\ndoing well",
    "I'm not\ndoing well"
]

FEELINGS = [
    'UN-\nCOMFORTABLE',
    'TIRED',
    'COLD',
    'HOT',
    'HAPPY',
    'SAD',
    'SICK',
    'ANNOYED'
]
