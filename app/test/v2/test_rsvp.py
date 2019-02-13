import os
import unittest
import json

from app import create_app
from ...db import get_db


class RSVPTestCase(unittest.TestCase):
    '''Test the RSVP endpoints'''
    def setUp(self):
        env = os.getenv('TEST_SETTINGS')
        self.app = create_app(env)

        with self.app.app_context():
            get_db(env)
        self.client = self.app.test_client()

        signup = {
            "fullname": "John Nyingi",
            "username": "j0nimost",
            "email": "j0ni@ke.com",
            "password": "**andela1",
            "confirmpassword": "**andela1",
            "role": 'admin'
        }

        self.meetup = {
            "topic": "Nairobi Golang",
            "location": "Senteru plaza",
            "happeningOn": "2019-01-26"
        }

        # Get token
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

    def test_create_rsvp(self):
        '''Test creating an rsvp for a meetup'''
        meetup_res = self.client.post('api/v2/meetups',
                                      data=json.dumps(self.meetup),
                                      headers=self.auth_header)
        self.assertEqual(meetup_res.status_code, 201)
        meetup = json.loads(meetup_res.data)
        meetupid = meetup['data'][0]['id']

        rsvp_res = self.client.post(
            'api/v2/meetups/{}/rsvp'.format(meetupid),
            headers=self.auth_header)
        self.assertEqual(rsvp_res.status_code, 202)
        rsvp = json.loads(rsvp_res.data)
        self.assertEqual(rsvp['message'],
                         'Successfully added to RSVP')
