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


@meetup_v2.route('/meetups/<int:meetup_id>/images', methods=['PATCH'])
@validate_input('images')
def post_images(meetup_id):
    images_ = request.json['images']
    # doess meetup exist
    meetup = meetup_obj.fetch('id', meetup_id)
    if meetup:
        '''update meetup'''
        id_ = meetup_obj.insert_images(meetup_id, images=images_)
        meetup_vals = meetup_obj.fetch('id', id_)
        meetup_keys = ['id', 'createdOn', 'topic', 'location', 'images',
                       'tags', 'happeningOn']
        meetup_dict = (zip(meetup_keys, meetup_vals))
        return jsonify(meetup_dict), 202
    else:
        notfound = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound), 404
