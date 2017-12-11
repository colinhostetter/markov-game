PLAYERS_PER_GAME = 2
WORDS_PER_SENTENCE = 10
ROUNDS_PER_GAME = 10
NUMBER_COMPUTER_SENTENCES = 2
MARKOV_STATE_SIZE = 2
OPTIONS_PRESENTED = 3

FIRST_WORD_CHOICE_TIME_SECONDS = 5
WORD_CHOICE_TIME_SECONDS = 3
GUESS_TIME_SECONDS = 10
REVEAL_TIME_SECONDS = 8
INACTIVITY_TIMEOUT_SECONDS = 5

COOKIE_NAME = 'markov'

GAME_STATUS_PREGAME = 'pregame'
GAME_STATUS_WRITING = 'writing'
GAME_STATUS_GUESS_TIME = 'guess_time'
GAME_STATUS_REVEAL = 'reveal'
GAME_STATUS_POSTGAME = 'postgame'

MESSAGE_JOINED_QUEUE = 'join_queue'
MESSAGE_GAME_READY = 'game_ready'

FALLBACK_WORDS = [
    'if', 'and', 'or', 'but', 'into', 'so', 'with', 'for'
]

with open('prompts.txt', 'r') as f:
    PROMPTS = f.read().split('\n')
