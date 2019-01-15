from flask import request, jsonify, make_response
from flask import Blueprint

from ..models.questionmodel import Questions
from ..utils.validation import validate_input

ques = Blueprint('ques', __name__, url_prefix='/api/v1')

quest_obj = Questions()


@ques.route('/questions', methods=['POST'])
@validate_input('question')
def post():
    '''Creates Question'''
    userid = request.json['userid']
    meetupid = request.json['meetupid']
    title = request.json['title']
    body = request.json['body']

    quest_obj.create_question(userid, meetupid, title, body)
    question_obj = quest_obj.return_data()
    question = {
        'status': 201,
        'data': [question_obj]
    }
    response = jsonify(question)
    response.status_code = 201
    return response


@ques.route('/questions/<int:id>/downvote', methods=['PATCH'])
@validate_input('vote')
def downvote(id):
    '''Downvotes a Question'''
    downvotes = request.json['votes']
    _, downvote_quest = quest_obj.find(id)
    if downvote_quest:
        question = quest_obj.update_votes(id, downvotes)
        question_obj = {
            'status': 202,
            'data': [question]
        }
        response = jsonify(question_obj)
        response.status_code = 202
        return response
    else:
        return jsonify(err_obj), 404


@ques.route('/questions/<int:id>/upvote', methods=['PATCH'])
@validate_input('vote')
def upvote(id):
    '''Upvotes a Question'''
    upvotes = request.json['votes']
    _, upvote_quest = quest_obj.find(id)
    if upvote_quest:
        question = quest_obj.update_votes(id, upvotes)
        question_obj = {
            'status': 202,
            'data': [question]
        }
        response = jsonify(question_obj)
        response.status_code = 202
        return response
    else:
        return jsonify(err_obj), 404

err_obj = {
    'status': 404,
    'error': 'Not Found'
}
