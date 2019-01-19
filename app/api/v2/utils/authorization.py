import os
import jwt
import datetime


def encode_jwt(userid):
    '''creates an encoded jwt token'''
    try:
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=0,
                                                              hours=1)
        creation = datetime.datetime.utcnow()

        payload = {
            "expiry": exp.isoformat(),
            "created": creation.isoformat(),
            "id": userid
        }
        token = jwt.encode(
            payload,
            os.getenv('SECRET'),
            algorithm='HS256').decode('utf-8')
        return token
    except Exception as e:
        return e


def decode_jwt(token):
    '''decode the jwt token'''
    try:
        payload = jwt.decode(token, os.getenv('SECRET'))
        return payload['id']
    except jwt.ExpiredSignatureError:
        return "Token is expired please login"
    except jwt.InvalidTokenError:
        return "Invalid Token please login"
