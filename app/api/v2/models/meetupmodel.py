import datetime
from .basemodel import BaseModel


class MeetupModel(BaseModel):
    '''Handles the business logic meetup'''
    def __init__(self):
        super().__init__('meetup')

    def insert_meetup_query(self, topic, location, happeningOn):
        '''creates the insert query'''
        createdOn = datetime.datetime.now()
        meetup_dict = {
            'createdOn': createdOn,
            'topic': topic,
            'location': location,
            'happeningOn': happeningOn
        }

        query = '''
                INSERT INTO {}(createdOn, topic, location, happeningOn)
                VALUES(%(createdOn)s, %(topic)s, %(location)s, %(happeningOn)s)
                RETURNING id;'''.format(self.table)
        id_ = super().insert(meetup_dict, query)
        return id_


meetup_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "location": {"type": "string"},
        "happeningOn": {"type": "string"}
    },
    "required": ["topic", "location", "happeningOn"]
}
