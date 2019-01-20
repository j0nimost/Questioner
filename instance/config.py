import os


class Config(object):
    '''Base Configuration class'''
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET = os.urandom(24)


class Production(Config):
    '''Production Environment variables'''
    DEBUG = False
    TESTING = False


class Testing(Config):
    '''Testing Environment Variables'''
    DEBUG = True
    TESTING = True
    # DATABASE_URL_TEST = os.getenv('DATABASE_URL_TEST')


class Development(Config):
    '''Development Environment Variables'''
    DEBUG = True


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
