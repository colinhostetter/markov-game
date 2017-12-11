import eventlet
import random
from copy import copy
from markovify.chain import END as MARKOVIFY_END_MARKER
from time import time

from app import constants
from app.markov import model

class Sentence(object):
    def __init__(self, words, is_player, options=None):
        self.words = words
        self.is_player = is_player
        self.options = options or []

    def __repr__(self):
        return f'<Sentence: words={self.words}, is_player={self.is_player}, options={self.options}>'

    def to_dict(self):
        return {'words': self.words, 'is_player': self.is_player, 'options': self.options}


class Game(object):
    """
    Object that captures the state of the game and handles round transitions, etc.
    No logic here that directly touches the sockets, that's handled by the handlers
    declared in the constructor
    """
    def __init__(self, socket_room, on_options_changed, on_sentence_finished, on_guess_made, on_game_ended,
                 on_player_went_inactive):
        self.guessing_player_index = random.randint(0, 1)
        self.round = 0
        self.word_num = 0
        self.players = []
        self.guesses_correct = []
        self.status = constants.GAME_STATUS_PREGAME
        self.active = True
        self.last_heartbeats = []

        self.socket_room = socket_room
        self.on_options_changed = on_options_changed
        self.on_sentence_finished = on_sentence_finished
        self.on_guess_made = on_guess_made
        self.on_game_ended = on_game_ended
        self.on_player_went_inactive = on_player_went_inactive

        eventlet.spawn_after(1, self._enforce_heartbeats_blocking)

    @property
    def player_sentence(self):
        return next(i for i in self.sentences if i.is_player)

    @property
    def computer_sentences(self):
        return [i for i in self.sentences if not i.is_player]

    @property
    def guessing_player(self):
        return self.players[self.guessing_player_index]

    @property
    def writing_player(self):
        index = 0 if self.guessing_player_index == 1 else 1
        return self.players[index]

    def join_game(self, player_id):
        self.players.append(player_id)
        self.last_heartbeats.append(time())

    def start_game(self):
        self.start_round(0)

    def start_round(self, round):
        self.round = round
        self.word_num = 0
        self.guessing_player_index = 1 if self.guessing_player_index == 0 else 0
        self.initialize_sentences()
        self.status = constants.GAME_STATUS_WRITING
        self.start_word(self.word_num)

    def start_word(self, word_num):
        self.word_num = word_num
        self.set_new_word_options()
        # print(self.sentences)
        self.on_options_changed(game=self)
        # Spawn a new coroutine to wait for the player's choice time to expire,
        # otherwise we will block this thread from receiving socket requests
        eventlet.spawn(self._wait_for_choice_blocking)

    def _wait_for_choice_blocking(self):
        current_round = self.round
        word_num = self.word_num
        sleep_time = constants.FIRST_WORD_CHOICE_TIME_SECONDS if word_num == 0 else constants.WORD_CHOICE_TIME_SECONDS
        eventlet.sleep(sleep_time)
        # See if the player made a choice while we were asleep. If they did,
        # this coroutine's work is done. If not, we should make a random choice.
        state_hasnt_changed = (
            self.active and
            self.round == current_round and
            self.word_num == word_num and
            self.status == constants.GAME_STATUS_WRITING
        )
        if state_hasnt_changed:
            word_index = random.randint(0, constants.OPTIONS_PRESENTED - 1)
            self.choose_word(word_index=word_index)

    def _wait_for_guess_blocking(self):
        current_round = self.round
        eventlet.sleep(constants.GUESS_TIME_SECONDS)
        # See if the guessing player made a guess while we were asleep. If they
        # did, this coroutine's work is done. If not, we should make a null guess.
        if self.active and self.round == current_round and self.status == constants.GAME_STATUS_GUESS_TIME:
            self.guess_sentence(sentence_index=None)

    def initialize_sentences(self):
        self.current_prompt = random.choice(constants.PROMPTS)
        words = self.current_prompt.split(' ')

        self.sentences = [
            Sentence(words=copy(words), is_player=False)
            for _ in range(constants.NUMBER_COMPUTER_SENTENCES)
        ]
        self.sentences.append(
            Sentence(words=copy(words), is_player=True)
        )
        random.shuffle(self.sentences)

    def set_new_word_options(self):
        # Sentences with the same state should get the same options
        slice_start = constants.MARKOV_STATE_SIZE * -1
        words_to_options = {
            ' '.join(s.words[slice_start:]): []
            for s in self.sentences
        }

        for words, options in words_to_options.items():
            lower_words = tuple(map(lambda word: word.lower(), words.split(' ')))

            # What words is it possible for us to present as options here?
            possible_options = model.chain.model[lower_words] if lower_words in model.chain.model else []
            # Don't count the "end sentence" marker as one of the options.
            num_possible_options = len(possible_options) - (1 if MARKOVIFY_END_MARKER in possible_options else 0)

            if num_possible_options < constants.OPTIONS_PRESENTED:
                # It's possible for a Markov chain to get into a dead end where there aren't
                # enough possible words for us to generate the options (sometimes even no
                # words at all). This can happen for two-word phrases that are very
                # uncommon in the corpus. In this case we need to fill the remaining space
                # in the options array with random small words that are "good enough".
                possible_fallbacks = list(set(constants.FALLBACK_WORDS) - set(possible_options))
                for _ in range(constants.OPTIONS_PRESENTED - num_possible_options):
                    options.append(random.choice(possible_fallbacks))

            while len(options) < constants.OPTIONS_PRESENTED:
                opt = model.chain.move(lower_words)
                if opt != MARKOVIFY_END_MARKER and opt not in options:
                    options.append(opt)

        for sentence in self.sentences:
            words = ' '.join(sentence.words[slice_start:])
            sentence.options = words_to_options[words]

    def choose_word(self, word_index):
        sentence = self.player_sentence
        sentence.words.append(sentence.options[word_index])
        self.choose_computer_words()
        if self.word_num + 1 < constants.WORDS_PER_SENTENCE:
            self.start_word(self.word_num + 1)
        else:
            self.status = constants.GAME_STATUS_GUESS_TIME
            self.on_sentence_finished(game=self)
            eventlet.spawn(self._wait_for_guess_blocking)

    def choose_computer_words(self):
        for sentence in self.sentences:
            if sentence.is_player:
                continue
            word = random.choice(sentence.options)
            sentence.words.append(word)

    def guess_sentence(self, sentence_index):
        if sentence_index is None:
            correct = None
            self.guesses_correct.append(None)
        else:
            correct = self.sentences[sentence_index].is_player
            self.guesses_correct.append(correct)
        self.status = constants.GAME_STATUS_REVEAL
        self.on_guess_made(game=self, sentence_index=sentence_index, correct=correct)
        eventlet.spawn(self._wait_out_reveal_time_blocking)

    def _wait_out_reveal_time_blocking(self):
        eventlet.sleep(constants.REVEAL_TIME_SECONDS)
        if self.active and self.round < constants.ROUNDS_PER_GAME - 1:
            self.start_round(self.round + 1)
        elif self.active:
            self.end_game()

    def end_game(self):
        self.on_game_ended(self)

    def heartbeat(self, player_id):
        index = self.players.index(player_id)
        self.last_heartbeats[index] = time()

    def _enforce_heartbeats_blocking(self):
        while self.active and self.status != constants.GAME_STATUS_POSTGAME:
            now = time()
            inactive_players = [
                player for index, player in enumerate(self.players)
                if now - self.last_heartbeats[index] > constants.INACTIVITY_TIMEOUT_SECONDS
            ]

            if len(self.players) > 1 and self.players[0] in inactive_players:
                self.on_player_went_inactive(game=self, player_id=self.players[0], other_player_id=self.players[1])
            if len(self.players) > 1 and self.players[1] in inactive_players:
                self.on_player_went_inactive(game=self, player_id=self.players[1], other_player_id=self.players[0])

            if len(inactive_players) == len(self.players):
                self.active = False
                self.on_game_ended(self, from_inactivity=True)
                return

            eventlet.sleep(1)
