from flask import jsonify, request
from flask import Blueprint

from ..models.commentmodel import CommentModel
from ..models.questionmodel import QuestionModel
from ..utils.authorization import isAuthorized, decode_jwt
from ..utils.validation import validate_input

commentv2 = Blueprint('commentv2', __name__, url_prefix='/api/v2')
ques_obj = QuestionModel()
comment_obj = CommentModel()


@commentv2.route('questions/<int:quesid>/comments', methods=['POST'])
@validate_input('comment')
@isAuthorized("")
def post(quesid):

    body = request.json['body']

    exists = ques_obj.exists('id', quesid)
    if exists:
        # Get userid
        token = request.headers.get('Authorization').split(" ")[1]
        userid, _ = decode_jwt(token)
        id_ = comment_obj.insert_comment(userid, quesid, body)
        comment = comment_obj.fetch('id', id_)
        comment_json = {
            "status": 201,
            "data": [comment]
        }
        return jsonify(comment_json), 201
    notfound = {
        "status": 404,
        "error": "Not Found"
    }
    return jsonify(notfound), 404