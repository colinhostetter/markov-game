from flask import send_file

def init_routes(app):
    app.add_url_rule('/', 'index', lambda: send_file('static/index.html'))
    app.add_url_rule('/game', 'game', lambda: send_file('static/game.html'))
