import os
import json
import unittest

from app import create_app
from ...api.v2.utils.authorization import encode_jwt
from ...db import get_db, drop_tables
from ...api.v2.models.meetupmodel import MeetupModel
from ...api.v2.models.usermodel import UserModel


class QuestionTestCase(unittest.TestCase):
    '''Tests for questions'''

    def setUp(self):
        '''set up data'''
        env = os.getenv('TEST_SETTINGS')
        self.app = create_app(env)

        with self.app.app_context():
            get_db(env)

        self.client = self.app.test_client()
        self.ques = {
            "topic": "Where is the meetup",
            "body": "I would like to know the venue of the meetup"
        }

        self.meetup = {
            "topic": "Nairobi Golang",
            "location": "Senteru plaza",
            "happeningOn": "2019-01-26"
        }

        signup = {
            "fullname": "John Nyingi",
            "username": "j0nimost",
            "email": "j0ni@ke.com",
            "password": "**andela1",
            "confirmpassword": "**andela1",
            "role": "admin"
        }

        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(signup),
                                    headers={
                                        "Content-Type": "application/json"})
        data = json.loads(response.data)
        self.token = data['data'][0]['token']

        self.auth_header = {
                            "Authorization": "bearer {}".format(self.token),
                            "Content-Type": "application/json"
                            }

    def test_create_question(self):
        '''Test create question'''
        meetup_res = self.client.post("api/v2/meetups",
                                      data=json.dumps(self.meetup),
                                      headers=self.auth_header)
        data = json.loads(meetup_res.data)
        id_ = data['data'][0]['id']
        response = self.client.post('api/v2/meetups/{}/questions'.format(id_),
                                    data=json.dumps(self.ques),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 201)

    def test_create_question_notfound(self):
        response = self.client.post('api/v2/meetups/0/questions',
                                    data=json.dumps(self.ques),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual("Meetup not found", data['error'])

    def tearDown(self):
        with self.app.app_context():
            drop_tables()
