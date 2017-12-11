import os
from flask import Flask
from flask_socketio import SocketIO

from app.game_manager import init_game_manager
from app.socket_handlers import init_socket_routes
from app.routes import init_routes

def initialize():
    print('Initializing app...')
    app = Flask(__name__, static_folder='static', static_url_path='/assets')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    socketio = SocketIO(app, async_mode='eventlet')
    init_routes(app)
    init_game_manager(socketio)
    init_socket_routes(socketio)
    socketio.run(app)

if __name__ == '__main__':
    initialize()
