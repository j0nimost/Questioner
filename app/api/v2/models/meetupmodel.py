import datetime
from .basemodel import BaseModel


class MeetupModel(BaseModel):
    '''Handles the business logic meetup'''

    def __init__(self):
        super().__init__('meetup')

    def insert_meetup_query(self, userid, topic, location, happeningOn=''):
        '''creates the insert query'''
        createdOn = datetime.datetime.now()
        meetup_dict = {
            'createdOn': createdOn,
            'topic': topic,
            'venue': location,
            'happeningOn': happeningOn
        }

        query = '''
                INSERT INTO {}(userid,createdOn, topic
                , venue, happeningOn)
                VALUES({}, %(createdOn)s, %(topic)s
                , %(venue)s, %(happeningOn)s)
                RETURNING id;'''.format(self.table, userid)
        id_ = super().insert(meetup_dict, query)
        return id_

    def insert_images(self, meetupid, images=[]):
        '''Update meetup and insert images'''
        meetup = super().fetch('id', meetupid)
        images = [('{' + x + '}',) for x in images]
        if meetup:
            query = '''
                        UPDATE meetup SET images=images || %s WHERE id={}
                        RETURNING id;
                    '''.format(meetupid)
            id_ = super().update(query, images)
            return id_
        return None

    def insert_tags(self, meetupid, tags=[]):
        '''Update meetup and insert tags'''
        meetup = super().fetch('id', meetupid)
        tags = [('{' + x + '}',) for x in tags]
        if meetup:
            query = '''
                        UPDATE meetup SET tags=tags || %s WHERE id={}
                        RETURNING id;
                    '''.format(meetupid)
            id_ = super().update(query, tags)
            return id_
        return None


class RsvpModel(BaseModel):
    '''Handles RSVP business logic'''
    def __init__(self):
        '''initialize db name'''
        super().__init__('rsvp')

    def insert_rsvp(self, userid: int, meetupid: int):
        '''Add meetup rsvp'''
        rsvp = {
            "userid": userid,
            "meetupid": meetupid
        }

        query = """INSERT INTO {table}(userid, meetupid)
                VALUES(%(userid)s, %(meetupid)s)
                ON CONFLICT DO NOTHING
                RETURNING id;""".format(table=self.table)
        id_ = super().insert(rsvp, query)
        return id_

meetup_schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "topic": {"type": "string",
                  "pattern": "^(\\s*\\w\\s*){2,}$"},
        "location": {"type": "string",
                     "pattern": "^(\\s*\\w\\s*){2,}$"},
        "happeningOn": {"type": "string",
                        "pattern": r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
                        }
    },
    "required": ["topic", "location", "happeningOn"]
}

image_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "images": {"type": "array",
                   "items": {"type": "string",
                             "pattern": "\w+:(\/?\/?)[^\s]+"},
                   "minItems": 1,
                   "maxItems": 4
                   }
    },
    "required": ["images"]
}

tags_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "tags": {"type": "array",
                 "items": {"type": "string",
                           "pattern": "^[A-Za-z]+$"},
                 "minItems": 1,
                 "maxItems": 4
                 }
    },
    "required": ["tags"]
}
