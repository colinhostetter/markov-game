import uuid
from copy import copy
from time import time

from app import constants
from app.game import Game

_game_registry = dict()
_queue = dict()
socketio = None


def init_game_manager(socketio_):
    global socketio
    socketio = socketio_

def create_game(game_id):
    game = Game(
        socket_room=game_id,
        on_options_changed=_send_state,
        on_sentence_finished=_send_state,
        on_guess_made=_on_guess_made,
        on_game_ended=_on_game_ended,
        on_player_went_inactive=_on_player_went_inactive
    )
    _game_registry[game_id] = game
    return game

def join_game(game_id, player_id):
    game = get_game(game_id=game_id)
    if not game:
        game = create_game(game_id=game_id)
    if len(game.players) < constants.PLAYERS_PER_GAME:
        game.join_game(player_id=player_id)
        if len(game.players) == constants.PLAYERS_PER_GAME:
            socketio.emit('game_starting', {'game_id': game_id}, room=game.socket_room)
            game.start_game()
    return game

def get_game(game_id):
    return _game_registry.get(game_id)

def choose_word(game_id, word_num, word_index, player_id):
    game = get_game(game_id=game_id)
    # Don't accept this choice unless it actually applies to this word
    valid = (
        game and
        game.writing_player == player_id and
        game.word_num == word_num and
        game.status == constants.GAME_STATUS_WRITING
    )
    if valid:
        game.choose_word(word_index=word_index)

def guess_sentence(game_id, player_id, sentence_index):
    game = get_game(game_id=game_id)
    valid = (
        game and
        game.guessing_player == player_id and
        game.status == constants.GAME_STATUS_GUESS_TIME
    )
    if valid:
        game.guess_sentence(sentence_index=sentence_index)

def join_queue(player_id):
    _queue[player_id] = {'last_heartbeat': time()}
    if len(_queue) > 1:
        make_games()
    else:
        socketio.emit(constants.MESSAGE_JOINED_QUEUE, room=player_id)

def make_games():
    now = time()
    while len(_queue) > 1:
        players = []
        for player_id in iter(copy(_queue)):
            player_data = _queue.pop(player_id)
            if now - player_data['last_heartbeat'] < constants.INACTIVITY_TIMEOUT_SECONDS:
                players.append(player_id)
            if len(players) == 2:
                break

        if len(players) == 1:
            _queue[player_id] = player_data
        else:
            game = create_game(make_game_id())
            message = {'game_id': game.socket_room}
            for player in players:
                socketio.emit(constants.MESSAGE_GAME_READY, message, room=player)

def make_game_id():
    return str(uuid.uuid4())

def game_heartbeat(game_id, player_id):
    game = get_game(game_id=game_id)
    if game:
        game.heartbeat(player_id=player_id)

def _serialize_game_state_for_guesser(game):
    return {
        'guesses_correct': game.guesses_correct,
        'round': game.round,
        'word_num': game.word_num,
        'sentences': [
            s.to_dict() if game.status == constants.GAME_STATUS_REVEAL else {'words': s.words}
            for s in game.sentences
        ],
        'guessing': True,
        'writing': False,
        'game_id': game.socket_room,
        'status': game.status
    }

def _seralize_game_state_for_writer(game):
    return {
        'guesses_correct': game.guesses_correct,
        'round': game.round,
        'word_num': game.word_num,
        'sentences': [s.to_dict() for s in game.sentences],
        'guessing': False,
        'writing': True,
        'game_id': game.socket_room,
        'status': game.status
    }

def _send_state(game):
    writing_player_message = _seralize_game_state_for_writer(game)
    guessing_player_message = _serialize_game_state_for_guesser(game)
    socketio.emit('game_state', writing_player_message, room=game.writing_player)
    socketio.emit('game_state', guessing_player_message, room=game.guessing_player)

def _on_guess_made(game, sentence_index, correct):
    _send_state(game=game)
    message = {
        'sentence_index': sentence_index,
        'correct': correct
    }
    socketio.emit('guess_made', message, room=game.socket_room)

def _on_game_ended(game, from_inactivity=False):
    if game.socket_room in _game_registry:
        del _game_registry[game.socket_room]
    if not from_inactivity:
        _send_state(game=game)
        message = {
            'game_id': game.socket_room,
            'guesses_correct': game.guesses_correct
        }
        socketio.emit('game_ended', message)

def _on_player_went_inactive(game, player_id, other_player_id):
    message = {'game_id': game.socket_room, 'player_id': player_id}
    socketio.emit('partner_inactive', message, room=other_player_id)

def queue_heartbeat(player_id):
    _queue[player_id] = {'last_heartbeat': time()}
    if len(_queue) >= 2:
        make_games()
