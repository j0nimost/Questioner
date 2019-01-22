from flask import jsonify, request
from flask import Blueprint

from ..models.meetupmodel import MeetupModel
from ..utils.validation import validate_input
meetup_v2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2')
meetup_obj = MeetupModel()


@meetup_v2.route('/meetups', methods=['POST'])
@validate_input('meetup')
def post():
    ''''create a meetup'''
    topic = request.json['topic']
    location = request.json['location']
    happeningOn = request.json['happeningOn']

    id_ = meetup_obj.insert_meetup_query(topic, location, happeningOn)
    meetup_vals = meetup_obj.fetch('id', id_)
    meetup_keys = ['id', 'createdOn', 'topic', 'location', 'images',
                   'tags', 'happeningOn']

    meetup_dict = dict(zip(meetup_keys, meetup_vals))
    # create response body
    meetup_dict = {
        "status": 201,
        "data": [meetup_dict]
    }
    return jsonify(meetup_dict), 201
