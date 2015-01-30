from flask import Flask
from app import config


def create_app(config_name):
    """TODO: Docstring for create_app.

    :config_name: TODO
    :returns: TODO

    """

    # start Flask app and load config
    app = Flask(__name__)
    config.config[config_name](app)

    #register all blueprints

    #init extensions

    #load all routes

    #auth token

    return app
