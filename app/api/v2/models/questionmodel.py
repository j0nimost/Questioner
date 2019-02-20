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

    def update_voteup(self, questionid: int, vote: int):
        '''Update vote up'''
        vote_ = {
            "questionid": questionid
        }

        query = '''UPDATE {table} SET voteup= COALESCE(voteup, 0) + {vote}
                    WHERE id=%(questionid)s RETURNING id;
                '''.format(table=self.table, vote=vote)

        id_ = super().update(query, vote_)
        return id_

    def update_votedown(self, questionid: int, vote: int):
        '''Update vote up'''
        vote_ = {
            "questionid": questionid
        }

        query = '''UPDATE {table} SET votedown= COALESCE(votedown, 0) + {vote}
                    WHERE id=%(questionid)s RETURNING id;
                '''.format(table=self.table, vote=vote)

        id_ = super().update(query, vote_)
        return id_

    def fetch_question(self, id: int):
        '''Fetch question and join the comments related'''

        questionid = {
            "id": id
        }

        query = ''' SELECT json_agg(quesag) AS json_object
                From (
                SELECT json_build_object('id', %(id)s, 'title', q.title,
                'body', q.body,
                'voteup', q.voteup,
                'votedown', q.votedown,
                'comments', json_agg(com.q)) AS quesag
                From {table} q
                LEFT JOIN(
                SELECT questionid, to_json(comment) AS q
                From comment) com ON com.questionid = %(id)s
                group By q.id, q.title, q.body) sub;
        '''.format(table=self.table)

        dbconn = super().db_instance()
        cursor = dbconn.cursor()
        cursor.execute(query, questionid)
        data = cursor.fetchone()
        cursor.close()
        return data


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
