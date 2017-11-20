from flask import render_template

def init_http_routes(app):
    app.add_url_rule('/', 'index', lambda: render_template('index.html'))
