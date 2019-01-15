from flask import request, jsonify, make_response
from flask import Blueprint


from ..models.commentmodel import Comments
from ..models.questionmodel import Questions
from ..utils.validation import validate_input

comment = Blueprint('comment', __name__, url_prefix='/api/v1')

comment_obj = Comments()
ques_obj = Questions()


@comment.route('/questions/<int:id>/comments', methods=['POST'])
@validate_input('comment')
def post(id):
    '''Create a comment endpoint'''
    _, question = ques_obj.find(id)
    if question:
        userid = request.json['userid']
        body = request.json['body']
        comment_obj.create_meetup(userid, id, body)
        data = comment_obj.return_data()
        data_response = {
            'status': 201,
            'data': data
        }
        response = jsonify(data_response)
        response.status_code = 201
        return response
    else:
        return make_response(jsonify({"message": "Not Found"}), 404)


@comment.route('/questions/<int:id>/comments', methods=['GET'])
def get(id):
    '''Get all comments under a question'''
    _, question = ques_obj.find(id)
    if question:
        comments = comment_obj.get_all(id)
        data = {
            'status': 200,
            'data': comments
        }
        response = jsonify(data)
        response.status_code = 200
        return response
    else:
        return make_response(jsonify({'message': 'Not Found'}), 404)
