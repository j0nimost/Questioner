import os
import jwt
import datetime
import json

from flask import jsonify
from functools import wraps
from flask import current_app, request
from ..models.usermodel import UserModel


def encode_jwt(userid, user_role='user'):
    '''creates an encoded jwt token'''
    try:
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=0,
                                                              hours=1)
        creation = datetime.datetime.utcnow()
        secret = current_app.config['SECRET']
        payload = {
            "expiry": exp.isoformat(),
            "created": creation.isoformat(),
            "id": userid,
            "role": user_role
        }
        token = jwt.encode(
            payload,
            secret,
            algorithm='HS256').decode('utf-8')
        return token
    except Exception as e:
        return e


def decode_jwt(token):
    '''decode the jwt token'''
    secret = current_app.config['SECRET']

    try:
        payload = jwt.decode(token, secret)
        return payload['id'], payload['role']
    except jwt.ExpiredSignatureError:
        return jsonify("Token is expired please login"), 400
    except jwt.InvalidTokenError:
        return jsonify("Invalid Token please login"), 400


def isAuthorized(role):
    '''checks users role to access an endpoint'''
    def decorator(func):
        wraps(func)

        def wrapper(*args, **kwargs):
            '''add validation logic'''
            user_obj = UserModel()
            header_ = request.headers.get('Authorization')
            if header_:
                try:
                    token = header_.split(" ")[1]
                except IndexError:
                    error = {
                        "status": 400,
                        "error": "malformed token"
                    }
                    return jsonify(error), 400

                userid, _ = decode_jwt(token)
                if isinstance(userid, int):
                    isvalid = user_obj.fetch("id", userid)
                    if isvalid:
                        if role:
                            if isvalid['userrole'] != role:
                                error_msg = {
                                    "status": 403,
                                    "error": "Unauthorized access"
                                }
                                return jsonify(error_msg), 403
                    else:
                        error_msg = {
                            "status": 400,
                            "error": "user does not exist"
                        }
                        return jsonify(error_msg), 400

                else:
                    error_tk = {
                        "status": 400,
                        "error": str(userid.json)
                    }
                    return jsonify(error_tk), 400
            else:
                error_msg = {
                    "status": 401,
                    "error": "Unauthenticated"
                }
                return jsonify(error_msg), 401
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
