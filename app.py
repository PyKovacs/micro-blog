from flask import Flask
from routes import blog_app, secret_key


def create_app():
    """ Flask app factory. """
    app = Flask(__name__)
    app.secret_key = secret_key
    app.register_blueprint(blog_app, url_prefix='/')
    return app
