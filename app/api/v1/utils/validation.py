from functools import wraps
from jsonschema import validate, ValidationError
from flask import request, current_app, jsonify

from .schema import config


def validate_input(schema):
    '''
    This is a decorator which will validate,
    all input is entered.
    '''
    def decorator(func):
        wraps(func)

        def wrapper(*args, **kwargs):
            '''deserialize to validate'''
            try:
                validate(request.json, config[schema])
            except ValidationError as e:
                return jsonify({"message": 'unexpected ' + e.message}), 400
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
