import os

from app import create_app

config = os.getenv('APP_SETTINGS')

if config:
    app = create_app(config)
else:
    config_ = os.getenv('FLASK_ENV')
    app = create_app(config_)

if __name__ == "__main__":
    app.run()
