from datetime import datetime as dt
from .basemodel import BaseModel


class CommentModel(BaseModel):
    '''This handles the business logic for comments'''
    def __init__(self):
        '''Initialize parent obj'''
        super().__init__('comment')

    def insert_comment(self, userid: int, questionid: int,
                       body: str):
        '''Insert comment build query'''
        comment = {
            'createdOn': dt.now(),
            'body': body
        }

        '''query'''
        comment_query = """
                        INSERT INTO {}(createdOn, userid, questionid, body)
                        VALUES(%(createdOn)s,{userid},{questionid},%(body)s)
                        RETURNING id;
        """.format(self.table, userid=userid, questionid=questionid)

        id_ = super().insert(comment, comment_query)
        return id_

    def update_comment(self, commentid: int, body: str):
        '''Update a comment'''
        comment = {
            "commentid": commentid,
            "body": body
        }

        update_query = '''UPDATE {table} SET body=%(body)s WHERE id=%(commentid)s
                       RETURNING id;'''.format(table=self.table)
        id_ = super().update(update_query, comment)
        return id_

comment_schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "body": {"type": "string",
                 "pattern": "^(?!\s*$).+",
                 "maxLength": 140}
    },
    "required": ["body"]
}
