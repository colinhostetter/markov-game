import eventlet
from unittest.mock import MagicMock
from unittest.mock import patch

from app import constants
from app.game import Game
from tests.app.base import BaseTestCase


class TestGame(BaseTestCase):
    def setUp(self):
        self.socket_room = 'you are tearing me apart lisa'
        self.on_options_changed = MagicMock()
        self.on_sentence_finished = MagicMock()
        self.on_guess_made = MagicMock()
        self.on_game_ended = MagicMock()
        self.game = Game(
            socket_room=self.socket_room,
            on_options_changed=self.on_options_changed,
            on_sentence_finished=self.on_sentence_finished,
            on_guess_made=self.on_guess_made,
            on_game_ended=self.on_game_ended
        )

    def test_join_game(self):
        player_id = 'abc'
        self.game.join_game(player_id=player_id)

        self.assertEqual(self.game.players, [player_id])
        self.assertEqual(self.game.status, constants.GAME_STATUS_PREGAME)

    def test_sentence_initialization(self):
        self.game.start_round(0)
        words = self.game.sentences[0].words
        options = self.game.sentences[0].options

        self.assertEqual(self.game.status, constants.GAME_STATUS_WRITING)
        self.assertCountEqual(
            [i.is_player for i in self.game.sentences],
            [False for _ in range(constants.NUMBER_COMPUTER_SENTENCES)] + [True]
        )
        for s in self.game.sentences:
            self.assertEqual(s.words, words)
            self.assertEqual(s.options, options)
        self.assertIn(' '.join(words), constants.PROMPTS)
        self.on_options_changed.assert_called_once()

    def test_choose_word(self):
        self.game.start_round(0)
        options = self.game.sentences[0].options
        word_index = 1
        self.assertEqual(self.game.status, constants.GAME_STATUS_WRITING)

        self.game.choose_word(word_index=word_index)

        self.assertEqual(self.game.status, constants.GAME_STATUS_WRITING)
        self.assertEqual(self.game.player_sentence.words[-1], options[word_index])
        for s in self.game.computer_sentences:
            self.assertIn(s.words[-1], options)
        self.assertEqual(self.on_options_changed.call_count, 2)

    def test_random_selection(self):
        _sleep = eventlet.sleep
        with patch('eventlet.sleep', side_effect=lambda _: _sleep(0.0001)):
            self.game.start_round(0)
            _sleep(0.0002)

        self.assertEqual(
            len(self.game.player_sentence.words),
            len(self.game.current_prompt.split(' ')) + 1
        )

    def test_guess_right_sentence(self):
        _sleep = eventlet.sleep
        self.game.start_round(0)

        right_index = self.game.sentences.index(self.game.player_sentence)
        with patch('eventlet.sleep', side_effect=lambda _: _sleep(0.001)):
            eventlet.spawn(lambda: self.game.guess_sentence(sentence_index=right_index))
            eventlet.sleep(0.001)
            self.on_guess_made.assert_called_once_with(game=self.game, sentence_index=right_index, correct=True)
            self.assertEqual(self.game.guesses_correct, [True])

    def test_guess_wrong_sentence(self):
        _sleep = eventlet.sleep
        self.game.start_round(0)

        wrong_index = self.game.sentences.index(self.game.computer_sentences[0])
        with patch('eventlet.sleep', side_effect=lambda _: _sleep(0.001)):
            eventlet.spawn(lambda: self.game.guess_sentence(sentence_index=wrong_index))
            eventlet.sleep(0.002)
            self.assertEqual(self.game.status, constants.GAME_STATUS_REVEAL)
            self.on_guess_made.assert_called_with(game=self.game, sentence_index=wrong_index, correct=False)
            self.assertEqual(self.game.guesses_correct, [False])

    def test_players_take_turns(self):
        self.game.join_game(player_id='a')
        self.game.join_game(player_id='b')
        self.game.start_round(0)
        first_guesser = self.game.guessing_player
        self.game.start_round(1)
        second_guesser = self.game.guessing_player
        self.assertNotEqual(first_guesser, second_guesser)
        self.assertCountEqual([first_guesser, second_guesser], self.game.players)

    def test_finish_sentence(self):
        self.game.start_round(0)
        self.game.word_num = constants.WORDS_PER_SENTENCE - 1

        self.game.choose_word(0)

        self.on_sentence_finished.assert_called_with(game=self.game)
        self.assertEqual(self.game.status, constants.GAME_STATUS_GUESS_TIME)