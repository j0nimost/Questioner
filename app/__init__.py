from flask import Flask

from instance.config import app_config


def create_app(config):
    '''Creates all Flask configurations and returns app.
    Expects config name'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config])
    app.config.from_pyfile('config.py', silent=True)
    return app
