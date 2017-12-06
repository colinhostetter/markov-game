from flask import Flask
from flask_socketio import SocketIO, emit

from app.game_manager import init_game_manager
from app.socket_handlers import init_socket_routes
from app.routes import init_routes

app = Flask(__name__, static_folder='static', static_url_path='/assets')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

if __name__ == '__main__':
    init_routes(app)
    init_game_manager(socketio)
    init_socket_routes(socketio)
    socketio.run(app, debug=True)
