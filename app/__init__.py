from flask import Flask

from instance.config import app_config

from .db import init
from .api.v1.views.meetupview import meetupreq
from .api.v1.views.questionview import ques
from .api.v1.views.commentview import comment

from .api.v2.views.userview import auth
from .api.v2.views.meetupview import meetup_v2 as meetupv2
from .api.v2.views.questionview import ques_v2

def create_app(config):
    '''Creates all Flask configurations and returns app.
    Expects config name'''
    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_SORT_KEYS'] = False
    app.config.from_object(app_config[config])
    # app.config.from_pyfile('config.py', silent=True)

    db = init(app.env)
    app.url_map.strict_slashes = False
    app.register_blueprint(auth)
    app.register_blueprint(meetupv2)
    app.register_blueprint(ques_v2)
    app.register_blueprint(meetupreq)
    app.register_blueprint(ques)
    app.register_blueprint(comment)

    return app
