from flask import request, jsonify, make_response
from flask import Blueprint

from ..models.questionmodel import Questions

ques = Blueprint('ques', __name__, url_prefix='/api/v1')

quest_obj = Questions()


@ques.route('/questions', methods=['POST'])
def post():
    '''Creates Question'''
    if request.json:
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

    else:
        return make_response(jsonify({"message": "invalid request type"}), 400)


@ques.route('/questions/<int:id>/downvote', methods=['PATCH'])
def downvote(id):
    '''Downvotes a Question'''
    if request.json:
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
            return make_response(jsonify({'message': 'Not Found'}), 404)
    else:
        return make_response(jsonify({'message': 'invalid request type'}))


@ques.route('/questions/<int:id>/upvote', methods=['PATCH'])
def upvote(id):
    '''Upvotes a Question'''
    if request.json:
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
            return make_response(jsonify({'message': 'Not Found'}), 404)
    else:
        return make_response(jsonify({'message': 'invalid request type'}))
