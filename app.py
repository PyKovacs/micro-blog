from flask import Flask

from source.configuration import secret_key
from source.routes import blog_app


def create_app():
    """ Flask app factory. """
    app = Flask(__name__)
    app.secret_key = secret_key
    app.register_blueprint(blog_app, url_prefix='/')
    return app
