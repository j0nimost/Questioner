from flask import jsonify, request
from flask import Blueprint

from ..utils.authorization import isAuthorized
from ..models.meetupmodel import MeetupModel
from ..utils.validation import validate_input
from ..utils.authorization import decode_jwt
meetup_v2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2')
meetup_obj = MeetupModel()


@meetup_v2.route('/meetups/upcoming', methods=['GET'])
@isAuthorized("")
def get_all():
    '''Get all upcoming meetups'''
    upcoming_meetups = meetup_obj.fetch_all_items()
    meetups = {
        "status": 200,
        "data": upcoming_meetups
    }
    return jsonify(meetups), 200


@meetup_v2.route('/meetups', methods=['POST'])
@validate_input('meetup')
@isAuthorized("admin")
def post():
    ''''create a meetup'''
    topic = request.json['topic']
    location = request.json['location']
    happeningOn = request.json['happeningOn']

    token = request.headers.get('Authorization').split(" ")[1]
    userid, _ = decode_jwt(token)

    exists = meetup_obj.exists('topic', topic)
    if exists:
        error_obj = {
            "status": 409,
            "error": "topic exists"
        }
        return jsonify(error_obj), 409
    id_ = meetup_obj.insert_meetup_query(userid, topic, location, happeningOn)
    meetup_ = meetup_obj.fetch('id', id_)
    # create response body
    meetup_dict = {
        "status": 201,
        "data": [meetup_]
    }
    return jsonify(meetup_dict), 201


@meetup_v2.route('/meetups/<int:meetup_id>/images', methods=['PATCH'])
@validate_input('images')
@isAuthorized("admin")
def post_images(meetup_id):
    images_ = request.json['images']
    # doess meetup exist
    meetup = meetup_obj.fetch('id', meetup_id)
    if meetup:
        '''update meetup'''
        id_ = meetup_obj.insert_images(meetup_id, images=images_)
        if isinstance(id_, bool):
            meetup_vals = meetup_obj.fetch('id', meetup_id)
            meetupid = meetup_vals['id']
            topic = meetup_vals['topic']
            images = meetup_vals['images']
            meetup_dict = {
                "status": 202,
                "data": {
                    "meetup_id": meetupid,
                    "topic": topic,
                    "images": images
                }
            }
            return jsonify(meetup_dict), 202
        else:
            return id_, 500
    else:
        notfound = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound), 404


@meetup_v2.route("/meetups/<int:meetup_id>/tags", methods=['PATCH'])
@validate_input("tags")
@isAuthorized("admin")
def post_tags(meetup_id):
    '''Adds tags'''
    tags = request.json['tags']
    # doess meetup exist
    meetup = meetup_obj.fetch('id', meetup_id)
    if meetup:
        '''update meetup'''
        id_ = meetup_obj.insert_tags(meetup_id, tags=tags)
        if isinstance(id_, bool):
            meetup_vals = meetup_obj.fetch('id', meetup_id)
            meetupid = meetup_vals['id']
            topic = meetup_vals['topic']
            tags = meetup_vals['tags']
            meetup_dict = {
                "status": 202,
                "data": {
                    "meetup_id": meetupid,
                    "topic": topic,
                    "tags": tags
                }
            }
            return jsonify(meetup_dict), 202
        else:
            return id_, 500
    else:
        notfound = {
            "status": 404,
            "error": "Not Found"
        }
        return jsonify(notfound), 404
