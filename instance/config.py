import os


class Config(object):
    '''Base Configuration class'''
    DEBUG = False


class Production(Config):
    '''Production Environment variables'''
    DEBUG = False
    TESTING = False


class Testing(Config):
    '''Testing Environment Variables'''
    DEBUG = True
    TESTING = True


class Development(Config):
    '''Development Environment Variables'''
    DEBUG = True


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
