from flask import request, jsonify, make_response
from flask import Blueprint
from werkzeug.exceptions import BadRequest

from ..models.meetupmodel import Meetups, RSVPS

meetupreq = Blueprint('meetupreq', __name__, url_prefix='/api/v1')

meetup_obj = Meetups()
rsvp_obj = RSVPS()


@meetupreq.route('/meetups', methods=['POST'])
def post():
    '''create meetup endup'''
    if request.json:
        topic = request.json['topic']
        location = request.json['location']
        images = request.json['images']
        happeningOn = request.json['happeningOn']
        tags = request.json['tags']

        meetup_obj.create_meetup(location, images, topic,
                                 happeningOn, tags)
        meetup_ = meetup_obj.return_data()
        response = jsonify(meetup_)
        response.status_code = 201
        return response
    else:
        return make_response(jsonify({'message': 'invalid request type'}), 400)


@meetupreq.route('/meetups/upcoming', methods=['GET'])
def get():
    '''Get all upcoming meetups'''
    meetups = meetup_obj.get_all()
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
    _, meetup_ = meetup_obj.find(id)
    if meetup_:
        meetup = {
            'status': 200,
            'data': [meetup_]
        }
        response = jsonify(meetup)
        response.status_code = 200
        return response
    return make_response(jsonify({"message": "Not Found"}), 404)


@meetupreq.route('/meetups/<int:id>/rsvps', methods=['POST'])
def post_rsvp(id):
    '''Create RSVP for an event'''
    _, meetup = meetup_obj.find(id)
    if request.json:
        if meetup:
            userid = request.json['userid']
            rsvp_obj.create_rsvp(userid, id)
            meetup_ = {
                'status': 201,
                'data': [meetup]
            }
            response = jsonify(meetup_)
            response.status_code = 201
            return response
        else:
            return make_response(jsonify({"message": "Not Found"}), 404)
    else:
        return make_response(jsonify({'message': 'invalid request type'}), 400)
