from flask import request, jsonify, make_response
from flask import Blueprint
from werkzeug.exceptions import BadRequest

from ..models.meetupmodel import Meetups, meetups

meetupreq = Blueprint('meetupreq', __name__, url_prefix='/api/v1')


@meetupreq.route('/meetups', methods=['POST'])
def post():
    '''create meetup endup'''
    if request.json:
        topic = request.json['topic']
        location = request.json['location']
        images = request.json['images']
        happeningOn = request.json['happeningOn']
        tags = request.json['tags']

        response = jsonify(Meetups().create_meetup(location, images, topic,
                           happeningOn, tags))
        response.status_code = 201
        return response
    else:
        return make_response(jsonify({'message': 'invalid request type'}), 400)


@meetupreq.route('/meetups/upcoming', methods=['GET'])
def get():
    '''Get all upcoming meetups'''
    upcomingmeetups = {
        'status': 200,
        'data': meetups
    }

    response = jsonify(upcomingmeetups)
    response.status_code = 200
    return response


@meetupreq.route('/meetups/<int:id>', methods=['GET'])
def get_by_id(id):
    '''Get a specific meetup with a particular ID'''
    meetup_obj = Meetups.find(id)
    if meetup_obj:
        meetup = {
            'status': 200,
            'data': [meetup_obj]
        }
        response = jsonify(meetup)
        response.status_code = 200
        return response
    return make_response(jsonify({"message": "Not Found"}), 404)


@meetupreq.route('/meetups/<int:id>/rsvps', methods=['POST'])
def post_rsvp(id):
    if request.json:
        if Meetups.find(id):
            userid = request.json['userid']
            meetup = Meetups.add_rsvp(userid, id)
            meetup_obj = {
                'status': 201,
                'data': [meetup]
            }
            response = jsonify(meetup_obj)
            response.status_code = 201
            return response
        else:
            return make_response(jsonify({"message": "Not Found"}), 404)
    else:
        return make_response(jsonify({'message': 'invalid request type'}), 400)
