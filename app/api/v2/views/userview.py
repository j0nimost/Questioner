from flask import request, jsonify
from flask import Blueprint
from flask_cors import cross_origin

from ..models.usermodel import UserModel
from ..utils.validation import validate_input, match_password
from ..utils.authorization import encode_jwt, decode_jwt
from ..utils.validation import hash_pass, check_pass

usr_obj = UserModel()
auth = Blueprint('auth', __name__, url_prefix='/api/v2')


@auth.route('/auth/signup', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
@validate_input('user')
def post():
    fullname = request.json['fullname']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_pass = request.json['confirmpassword']

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
    _id = usr_obj.insert_query(fullname, username, email, h_password)
    if _id:
        '''create token'''
        usr = usr_obj.fetch('id', _id)
        usr_val = list(usr)
        token = encode_jwt(_id)
        user_key = ['id', 'firstname', 'lastname', 'username', 'email',
                    'password', 'createdOn']
        usr_dict = dict(zip(user_key, usr_val))
        token_body = {
            "status": 201,
            "data": [
                {
                    "token": token,
                    "user": [usr_dict]
                }
            ]
        }
        if isinstance(token, str):
            return jsonify(token_body), 201
    return jsonify(_id), 400
