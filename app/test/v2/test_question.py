import json
import unittest

from app import create_app
from ...api.v2.utils.authorization import encode_jwt
from ...db import create_query, exec_queries, delete_test
from ...api.v2.models.meetupmodel import MeetupModel
from ...api.v2.models.usermodel import UserModel


class QuestionTestCase(unittest.TestCase):
    '''Tests for questions'''

    def setUp(self):
        '''set up data'''
        self.app = create_app("testing")
        self.client = self.app.test_client()
        queries = create_query()
        exec_queries(queries)
        self.ques = {
            "topic": "Where is the meetup",
            "body": "I would like to know the venue of the meetup"
        }
        
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.usr),
                                    content_type="application/json")
                                    
        data = json.loads(response.data)
        print(data)
        self.userid = data['data'][0]['user'][0]['id']
        self.id_ = MeetupModel().insert_meetup_query(
                                                     self.userid,
                                                     'Nairobi Go lang',
                                                     'Senteru plaza',
                                                     '2019-01-26')
        self.auth_header = {
                            "Authorization": "bearer {}".format(data['token']),
                            "Content-Type": "application/json"
                            }

    def test_create_question(self):
        '''Test create question'''
        response = self.client.post('api/v2/meetups/{}/question'.format(self.userid),
                                    data=json.dumps(self.ques),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 201)

    def test_create_question_notfound(self):
        response = self.client.post('api/v2/meetups/0/question',
                                    data=json.dumps(self.ques),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual("Meetup not found", data['error'])

    def tearDown(self):
        queries = delete_test()
        exec_queries(queries)
