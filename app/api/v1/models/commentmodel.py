import datetime

from .basemodel import BaseModel, comments


class Comments(BaseModel):
    '''
    The Comment Model Class defines the business logic
    '''
    def __init__(self):
        '''Initialize db'''
        super().__init__('commentdb')

    def create_meetup(self, userid: int, questionid: int,
                      body: str):
        '''Create a comment'''
        comment = {
            'id': len(comments)+1,
            'time': str(datetime.datetime.now()),
            'userid': userid,
            'questionid': questionid,
            'body': body
        }
        self.save(comment)

comment_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "userid": {"type": "number"},
        "body": {"type": "string"}
    },
    "required": ["userid", "body"]
}
