from . import urlshort
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "!(<bzTt<aw-$#{>"
    # app.SECRET_KEY = "secret"

    app.register_blueprint(urlshort.bp)

    return app
