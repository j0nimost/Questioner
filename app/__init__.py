from flask import Flask

from instance.config import app_config

from .api.v1.views.meetupview import meetupreq
from .api.v1.views.questionview import ques


def create_app(config):
    '''Creates all Flask configurations and returns app.
    Expects config name'''
    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_SORT_KEYS'] = False
    app.config.from_object(app_config[config])
    app.config.from_pyfile('config.py', silent=True)

    app.register_blueprint(meetupreq)
    app.register_blueprint(ques)
    return app
