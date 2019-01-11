from flask import request, jsonify, make_response
from flask import Blueprint

from ..models.questionmodel import Questions

ques = Blueprint('ques', __name__, url_prefix='/api/v1')


@ques.route('/questions', methods=['POST'])
def post():
    '''Creates Question'''
    if request.json:
        userid = request.json['userid']
        meetupid = request.json['meetupid']
        title = request.json['title']
        body = request.json['body']

        question_obj = Questions.create_question(userid, meetupid, title, body)
        question = {
            'status': 201,
            'data': [question_obj]
        }
        response = jsonify(question)
        response.status_code = 201
        return response

    else:
        return make_response(jsonify({"message": "invalid request type"}), 400)


@ques.route('/questions/<int:id>/downvote', methods=['PATCH'])
def downvote(id):
    '''Downvotes a Question'''
    if request.json:
        votes = request.json['votes']
        _, find_question = Questions.find(id)
        if find_question:
            question = Questions.update(id, votes)
            question_obj = {
                'status': 202,
                'data': [question]
            }
            response = jsonify(question_obj)
            response.status_code = 202
            return response
        else:
            return make_response(jsonify({'message': 'Not Found'}), 404)
    else:
        return make_response(jsonify({'message': 'invalid request type'}))
