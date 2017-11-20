from flask import Flask
from flask_socketio import SocketIO, emit

from app.http_handlers.routes import init_http_routes
from app.socket_handlers import init_socket_routes
from app.game_manager import init_game_manager

app = Flask(__name__, static_folder='dist', static_url_path='/assets')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

if __name__ == '__main__':
    init_game_manager(socketio)
    init_http_routes(app)
    init_socket_routes(socketio)
    socketio.run(app, debug=True)
