from flask import request, jsonify, make_response
from flask import Blueprint
from werkzeug.exceptions import BadRequest

from ..models.meetupmodel import Meetups, RSVPS
from ..utils.validation import validate_input

meetupreq = Blueprint('meetupreq', __name__, url_prefix='/api/v1')

meetup_obj = Meetups()
rsvp_obj = RSVPS()


@meetupreq.route('/meetups', methods=['POST'])
@validate_input('meetup')
def post():
    '''create meetup endup'''
    topic = request.json['topic']
    location = request.json['location']
    images = request.json['images']
    happeningOn = request.json['happeningOn']
    tags = request.json['tags']

    meetup_obj.create_meetup(location, images, topic,
                             happeningOn, tags)
    meetup_ = meetup_obj.return_data()
    response_obj = {
        "status": 201,
        "data": [meetup_]
    }
    response = jsonify(response_obj)
    response.status_code = 201
    return response


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
    return jsonify(err_obj), 404


@meetupreq.route('/meetups/<int:id>', methods=['PATCH'])
@validate_input('meetup')
def update(id):
    '''Update a meetup'''
    update_meetup = request.json
    _, meetup_ = meetup_obj.find(id)
    if meetup_:
        data = meetup_obj.update(update_meetup)
        meetup_upd = {
            'status': 202,
            'data': data
        }
        response = jsonify(meetup_upd)
        response.status_code = 202
        return response
    else:
        return jsonify(err_obj), 404


@meetupreq.route('/meetups/<int:id>', methods=['DELETE'])
def delete(id):
    '''Delete a meetup'''
    _, meetup = meetup_obj.find(id)
    if meetup:
        meetup_obj.delete(id)
        message = {
            'status': 200,
            'data': "Successfully Deleted"
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    else:
        return jsonify(err_obj), 404


@meetupreq.route('/meetups/<int:id>/rsvps', methods=['POST'])
@validate_input('rsvp')
def post_rsvp(id):
    '''Create RSVP for an event'''
    _, meetup = meetup_obj.find(id)
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
        return jsonify(err_obj), 404

err_obj = {
    'status': 404,
    'error': 'Not Found'
}
