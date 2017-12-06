from unittest.mock import patch

from app import constants
from app import game_manager
from app.game import Game
from tests.app.base import BaseTestCase


class TestGameManager(BaseTestCase):
    def _setup_game(self):
        game_id = 'abcdef'
        game_manager.create_game(game_id=game_id)
        game_manager.join_game(game_id=game_id, player_id='1')
        return game_manager.join_game(game_id=game_id, player_id='2')

    def test_create_and_get_game(self):
        game_id = 'abcdef'
        game = game_manager.create_game(game_id=game_id)

        self.assertEqual(type(game), Game)
        self.assertEqual(game.status, constants.GAME_STATUS_PREGAME)

        got_game = game_manager.get_game(game_id=game_id)

        self.assertEqual(game, got_game)

    def test_get_missing_game(self):
        game = game_manager.get_game('asdfsdaf')
        self.assertIsNone(game)

    def test_join_game(self):
        game_id = 'abcdef'
        player_id = 'xyz'
        player2_id = '123'

        game_manager.create_game(game_id=game_id)
        game = game_manager.join_game(game_id=game_id, player_id=player_id)

        self.assertEqual(game.players, [player_id])
        self.assertEqual(game.status, constants.GAME_STATUS_PREGAME)

        # Should start when a second player joins
        game = game_manager.join_game(game_id=game_id, player_id=player2_id)
        self.assertEqual(game.status, constants.GAME_STATUS_WRITING)
        self.assertCountEqual(game.players, [player_id, player2_id])
        self.assertEqual(self.emissions[0].name, 'game_state')
        self.assertEqual(self.emissions[1].name, 'game_state')
        self.assertCountEqual(
            [i.room for i in self.emissions],
            game.players
        )

    def test_choose_word(self):
        game = self._setup_game()
        word = game.player_sentence.options[1]

        game_manager.choose_word(
            game_id=game.socket_room,
            word_num=0,
            word_index=1,
            player_id=game.writing_player
        )

        self.assertEqual(game.player_sentence.words[-1], word)
        self.assertEqual(game.word_num, 1)

    def test_bad_choose_word(self):
        game = self._setup_game()

        # wrong player
        game_manager.choose_word(
            game_id=game.socket_room,
            word_num=0,
            word_index=1,
            player_id=game.guessing_player
        )

        # word_num doesn't match game state
        game_manager.choose_word(
            game_id=game.socket_room,
            word_num=1,
            word_index=1,
            player_id=game.writing_player
        )

        # wrong status
        game.status = constants.GAME_STATUS_GUESS_TIME
        game_manager.choose_word(
            game_id=game.socket_room,
            word_num=0,
            word_index=1,
            player_id=game.guessing_player
        )
        game.status = constants.GAME_STATUS_WRITING

        # invalid game
        game_manager.choose_word(
            game_id='tktktk',
            word_num=0,
            word_index=1,
            player_id=game.writing_player
        )

        self.assertEqual(game.word_num, 0)

    def test_guess_sentence(self):
        game = self._setup_game()
        game.status = constants.GAME_STATUS_GUESS_TIME

        game_manager.guess_sentence(
            game_id=game.socket_room,
            player_id=game.guessing_player,
            sentence_index=0
        )

        self.assertEqual(len(game.guesses_correct), 1)

    def test_bad_guess_sentence(self):
        game = self._setup_game()
        game.status = constants.GAME_STATUS_GUESS_TIME

        # wrong player
        game_manager.guess_sentence(
            game_id=game.socket_room,
            player_id=game.writing_player,
            sentence_index=0
        )

        # invalid game
        game_manager.guess_sentence(
            game_id='tktktk',
            player_id=game.guessing_player,
            sentence_index=0
        )

        # wrong status
        game.status = constants.GAME_STATUS_WRITING
        game_manager.choose_word(
            game_id=game.socket_room,
            word_num=0,
            word_index=1,
            player_id=game.guessing_player
        )
        game.status = constants.GAME_STATUS_GUESS_TIME

        self.assertEqual(len(game.guesses_correct), 0)

    def test_join_queue(self):
        players = ['a', 'b']

        game_manager.join_queue(player_id=players[0])

        first_emission = self.mock_socketio.emit.call_args_list[0]
        self.assertEqual(first_emission[0], (constants.MESSAGE_JOINED_QUEUE,))
        self.assertEqual(first_emission[1], {'room': players[0]})

        game_manager.join_queue(player_id=players[1])

        emissions = self.mock_socketio.emit.call_args_list[1:3]
        self.assertEqual(emissions[0][1], {'room': players[0]})
        self.assertEqual(emissions[1][1], {'room': players[1]})
        self.assertEqual(emissions[0][0][1]['game_id'], emissions[1][0][1]['game_id'])
