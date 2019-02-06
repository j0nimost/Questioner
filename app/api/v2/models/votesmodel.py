from .basemodel import BaseModel


class VoteUpModel(BaseModel):
    '''Handles upvote business logic'''
    def __init__(self):
        super().__init__('voteup')

    def insert_voteup(self, questionid: int, userid: int):
        '''inserts vote registers the user'''
        voteup = {
            "questionid": questionid,
            "userid": userid
        }

        query = ''' INSERT INTO {table}(questionid, userid)
                    VALUES(%(questionid)s, %(userid)s)
                    ON CONFLICT DO NOTHING RETURNING id;
            '''.format(table=self.table)
        id_ = super().insert(voteup, query)
        return id_

votes_schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "vote": {"type": "integer",
                 "minimum": 0,
                 "maximum": 2,
                 "exclusiveMinimum": True,
                 "exclusiveMaximum": True
                 }
    },
    "required": ["vote"]
}
