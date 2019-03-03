from flask import request, jsonify
from flask import Blueprint

from ..models.usermodel import UserModel
from ..utils.validation import validate_input, match_password
from ..utils.authorization import encode_jwt, decode_jwt
from ..utils.validation import hash_pass, check_pass

usr_obj = UserModel()
auth = Blueprint('auth', __name__, url_prefix='/api/v2')


@auth.route('/auth/signup', methods=['POST'])
@validate_input('user')
def post():
    fullname = request.json['fullname']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_pass = request.json['confirmpassword']

    try:
        userrole = request.json['role']
    except KeyError:
        userrole = 'user'

    isMatched = match_password(password, confirm_pass)
    if not isMatched:
        error = {
            "status": 400,
            "error": "password and confirm password don't match"
        }
        return jsonify(error), 400

    usr1 = usr_obj.exists('email', email)
    usr2 = usr_obj.exists('username', username)
    if usr1 or usr2:
        err_obj = {
            "status": 409,
            "error": "user already exists with similar email/username"
        }
        return jsonify(err_obj), 409

    h_password = hash_pass(password)

    if userrole:
        _id = usr_obj.insert_query(fullname, username, email, h_password,
                                   userrole)
    else:
        _id = usr_obj.insert_query(fullname, username, email, h_password)
    if _id:
        '''create token'''
        usr = usr_obj.fetch('id', _id)
        if userrole:
            token = encode_jwt(_id, userrole)
        else:
            token = encode_jwt(_id)
        token_body = {
            "status": 201,
            "data": [
                {
                    "token": token,
                    "user": [usr]
                }
            ]
        }
        if isinstance(token, str):
            return jsonify(token_body), 201
    return jsonify(_id), 400


@auth.route('auth/signin', methods=['POST'])
@validate_input('login')
def login():
    '''This is the login endpoint'''
    email = request.json['email']
    password = request.json['password']

    usr = usr_obj.fetch('email', email)
    if usr:
        isPassword = check_pass(usr['password'], password)
        if isPassword:
            if usr['userrole'] == 'admin':
                token = encode_jwt(usr['id'], 'admin')
            else:
                token = encode_jwt(usr['id'])
            token_body = {
                "status": 202,
                "data": [{
                    "token": token,
                    "user": [usr]
                }]
            }
            return jsonify(token_body), 202
    return jsonify(error), 400

error = {
        "status": 400,
        "error": "Wrong password/email"
        }
