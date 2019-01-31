from flask import request, jsonify
from flask import Blueprint

from ..utils.authorization import isAuthorized
from ..utils.validation import validate_input
from ..models.questionmodel import QuestionModel
from ..models.meetupmodel import MeetupModel
from ..utils.authorization import decode_jwt

ques_obj = QuestionModel()
meetup_obj = MeetupModel()
ques_v2 = Blueprint("ques_v2", __name__, url_prefix="/api/v2")


@ques_v2.route("meetups/<int:meetup_id>/questions", methods=['POST'])
@validate_input('ques')
@isAuthorized("")
def create_ques(meetup_id):
    topic = request.json['topic']
    body = request.json['body']

    exists = meetup_obj.exists('id', meetup_id)
    if not exists:
        error_obj = {
            "status": 404,
            "error": "Meetup not found"
        }
        return jsonify(error_obj), 404
    # valid
    token = request.headers.get('Authorization').split(" ")[1]
    userid, _ = decode_jwt(token)

    id_ = ques_obj.insert_question_query(meetup_id, userid, topic, body=body)
    ques_dict = ques_obj.fetch('id', id_)
    ques_json = {
        "status": 201,
        "data": [ques_dict]
    }
    return jsonify(ques_json), 201
