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

    def delete_voteup(self, id_: int):
        '''Delete an existing upvote'''
        result = super().delete(self.table, id_)
        return result


class VoteDownModel(BaseModel):
    '''Handles downvote business logic'''
    def __init__(self):
        super().__init__('votedown')

    def insert_votedown(self, questionid: int, userid: int):
        '''inserts vote down'''

        votedown = {
            "questionid": questionid,
            "userid": userid
        }

        query_ = ''' INSERT INTO {table}(questionid, userid)
                     VALUES(%(questionid)s, %(userid)s)
                     ON CONFLICT DO NOTHING RETURNING id;
                     '''.format(table=self.table)

        id_ = super().insert(votedown, query_)
        return id_

    def delete_votedown(self, id_: int):
        '''Delete an existing voteup'''
        result = super().delete(self.table, id_)
        return result

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
