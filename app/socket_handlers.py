from flask import request, session
from flask_socketio import emit, join_room

from app import constants
from app import game_manager


def init_socket_routes(socketio):
    @socketio.on('connect')
    def connect():
        user_id = request.cookies.get(constants.COOKIE_NAME)
        session['user_id'] = user_id
        join_room(user_id)

    @socketio.on('heartbeat')
    def heartbeat():
        emit('thump')

    @socketio.on('join_game')
    def join_game(data):
        game_id = data['game_id']
        join_room(game_id)
        game_manager.join_game(game_id=game_id, player_id=session['user_id'])

    @socketio.on('choose_word')
    def choose_word(data):
        game_manager.choose_word(
            game_id=data['game_id'],
            word_num=data['word_num'],
            word_index=data['word_index'],
            player_id=session['user_id']
        )

    @socketio.on('guess_sentence')
    def guess_sentence(data):
        game_manager.guess_sentence(
            game_id=data['game_id'],
            sentence_index=data['sentence_index'],
            player_id=session['user_id']
        )

    @socketio.on('join_queue')
    def join_queue():
        game_manager.join_queue(player_id=session['user_id'])
