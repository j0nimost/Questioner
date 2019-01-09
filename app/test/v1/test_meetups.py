import unittest
import json

from app import create_app
from ...api.v1.models.meetups import Meetups, meetups


class MeetupsTestCase(unittest.TestCase):
    '''These are the test cases for meetups features'''
    def setUp(self):
        self.app = create_app(config='development')
        self.client = self.app.test_client()

        self.meetup = {
            'id': 1,
            'createdOn': '2019-01-09',
            'location': 'IHub',
            'images': [],
            'topic': 'Nairobi Go Meetup',
            'happeningOn': '2019-01-26',
            'tags': []
        }

        meetups.append(self.meetup)

    def test_create_meetup(self):
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_create_meetup_badrequest(self):
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request type', str(json.loads(response.data)))

