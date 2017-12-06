import uuid

from app import constants
from app.game import Game


_game_registry = dict()
_queue = set()
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
        on_game_ended=_on_game_ended
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
    _queue.add(player_id)
    if len(_queue) > 1:
        make_games()
    else:
        socketio.emit(constants.MESSAGE_JOINED_QUEUE, room=player_id)

def make_games():
    while len(_queue) > 1:
        players = [_queue.pop(), _queue.pop()]
        game = create_game(make_game_id())
        message = {'game_id': game.socket_room}
        for player in players:
            socketio.emit(constants.MESSAGE_GAME_READY, message, room=player)

def make_game_id():
    return str(uuid.uuid4())

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

def _on_game_ended(game):
    _send_state(game=game)
    message = {
        'final_score': len([i for i in game.guesses_correct if i is True])
    }
    socketio.emit('game_ended', message)
