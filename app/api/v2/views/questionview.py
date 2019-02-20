from flask import request, jsonify
from flask import Blueprint

from ..utils.authorization import isAuthorized
from ..utils.validation import validate_input
from ..models.questionmodel import QuestionModel
from ..models.meetupmodel import MeetupModel
from ..models.votesmodel import VoteUpModel, VoteDownModel
from ..utils.authorization import decode_jwt

meetup_obj = MeetupModel()
ques_obj = QuestionModel()

ques_v2 = Blueprint("ques_v2", __name__, url_prefix="/api/v2")


@ques_v2.route('questions/<int:quesid>', methods=['GET'])
@isAuthorized("")
def get_question(quesid):
    '''Get individual question'''
    exists = ques_obj.exists('id', quesid)

    if exists:
        data = ques_obj.fetch_question(quesid)[0]

        question = {
            "status": 200,
            "data": data
        }

        return jsonify(question), 200
    else:
        notfound = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound), 404


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


@ques_v2.route('questions/<int:ques_id>/upvote', methods=['PATCH'])
@validate_input('vote')
@isAuthorized("")
def question_upvote(ques_id):
    '''Upvote a Question'''
    voteup_obj = VoteUpModel()

    vote = request.json['vote']

    token = request.headers.get('Authorization').split(" ")[1]
    userid, _ = decode_jwt(token)

    exists = ques_obj.exists('id', ques_id)
    if exists:
        # add vote
        vote_id = voteup_obj.insert_voteup(ques_id, userid)
        if vote_id:
            votedown = VoteDownModel()
            downvote_exists = votedown.fetch_multiple_ids('questionid',
                                                          ques_id,
                                                          'userid', userid)
            if downvote_exists:
                # delete votedown
                _ = votedown.delete(downvote_exists['id'])
                vote_update = -1
                _ = ques_obj.update_votedown(ques_id, vote_update)

            # increment vote
            q_id = ques_obj.update_voteup(ques_id, vote)
            # Fetch question
            question = ques_obj.fetch('id', q_id)
            question_json = {
                "status": 202,
                "data": [question]
            }
            return jsonify(question_json), 202
        else:
            vote_json = {
                "status": 400,
                "error": "You already voted"
            }
            return jsonify(vote_json), 400
    else:
        notfound_json = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound_json), 404


@ques_v2.route('questions/<int:ques_id>/downvote', methods=['PATCH'])
@validate_input('vote')
@isAuthorized("")
def question_downvote(ques_id):
    '''Upvote a Question'''
    votedown_obj = VoteDownModel()

    vote = request.json['vote']

    token = request.headers.get('Authorization').split(" ")[1]
    userid, _ = decode_jwt(token)

    exists = ques_obj.exists('id', ques_id)
    if exists:
        # add vote
        vote_id = votedown_obj.insert_votedown(ques_id, userid)

        if vote_id:

            voteup = VoteUpModel()
            upvote_exists = voteup.fetch_multiple_ids('questionid', ques_id,
                                                      'userid', userid)
            if upvote_exists:
                _ = voteup.delete(upvote_exists['id'])
                vote_update = -1
                _ = ques_obj.update_voteup(ques_id, vote_update)

            q_id = ques_obj.update_votedown(ques_id, vote)
            # Fetch question
            question = ques_obj.fetch('id', q_id)
            question_json = {
                "status": 202,
                "data": [question]
            }
            return jsonify(question_json), 202
        else:
            vote_json = {
                "status": 400,
                "error": "You already voted"
            }
            return jsonify(vote_json), 400
    else:
        notfound_json = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound_json), 404


@ques_v2.route('questions/<int:quesid>', methods=['DELETE'])
@isAuthorized("")
def delete(quesid):
    '''Delete a question'''
    exists = ques_obj.exists('id', quesid)

    if exists:
        token = request.headers.get('Authorization').split(" ")[1]
        userid, _ = decode_jwt(token)

        ques = ques_obj.fetch('id', quesid)

        if ques['userid'] == userid:
            _ = ques_obj.delete(quesid)
            return jsonify(), 204

        notallowed = {
            "status": 405,
            "error": "only question creater can delete"
        }
        return jsonify(notallowed), 405

    else:
        notfound = {
            "status": 404,
            "error": "Not Found"
        }

        return jsonify(notfound), 404
