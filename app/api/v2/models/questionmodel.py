from .basemodel import BaseModel


class QuestionModel(BaseModel):
    '''Handles business logic for questions'''

    def __init__(self):
        '''Initialize table name'''
        super().__init__('question')
 
    def insert_question_query(self, meetupid: int, userid: int, title='',
                              body=''):
        '''creates the insert query'''
        question_dict = {
            'title': title,
            'body': body
        }

        query = '''
                INSERT INTO {}(meetupid, userid, title
                , body)
                VALUES({},{},%(title)s,%(body)s)
                RETURNING id;'''.format(self.table, meetupid, userid)
        id_ = super().insert(question_dict, query)
        return id_


question_schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "userid": {"type": "number"},
        "meetupid": {"type": "number"},
        "topic": {"type": "string",
                  "pattern": "^(\\s*\\w\\s*){2,}$"},
        "body": {"type": "string",
                 "pattern": "^(\\s*\\w\\s*){2,}$"}
    },
    "required": ["topic", "body"]
}
