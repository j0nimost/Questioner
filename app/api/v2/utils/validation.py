from functools import wraps
from jsonschema import validate, ValidationError
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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
                if e.validator == 'pattern':
                    err_obj = {
                        "status": 400,
                        "error": 'unexpected pattern for ' + e.path[0]
                    }
                elif e.validator == 'minLength':
                    err_obj = {
                        "status": 400,
                        "error": 'unexpected {} too short'.format(e.path[0])
                    }
                else:
                    err_obj = {
                        "status": 400,
                        "error": 'unexpected ' + e.message
                    }
                return jsonify(err_obj), 400
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


def match_password(password, confirm_pass):
    '''check if passwords match'''
    if password == confirm_pass:
        return True
    else:
        return False


def hash_pass(password):
    '''creates hash'''
    return generate_password_hash(password)


def check_pass(hash_pass, password):
    '''checks if password'''
    isPass = check_password_hash(hash_pass, password)
    return isPass
