import unittest
import json

from app import create_app
from ...api.v1.models.meetupmodel import Meetups, meetups


class MeetupsTestCase(unittest.TestCase):
    '''These are the test cases for meetups features'''
    def setUp(self):
        self.app = create_app(config='development')
        self.client = self.app.test_client()

        self.meetup = {
            'location': 'IHub',
            'images': [],
            'topic': 'Nairobi Go Meetup',
            'happeningOn': '2019-01-26',
            'tags': []
        }

        meetups.append({
            'id': 1,
            'createdOn': '2019-01-09',
            'location': 'IHub',
            'images': [],
            'topic': 'Nairobi Go Meetup',
            'happeningOn': '2019-01-26',
            'tags': []
        })

    def test_create_meetup(self):
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print('{} code'.format(response.status_code))
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_create_meetup_badrequest(self):
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid request type', str(json.loads(response.data)))

    def test_get_upcoming(self):
        response = self.client.get('/api/v1/meetups/upcoming')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_get_meetup(self):
        response = self.client.get('/api/v1/meetups/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_get_meetup_notfound(self):
        response = self.client.get('/api/v1/meetups/0')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not Found', str(json.loads(response.data)))

    def tearDown(self):
        meetups.pop()
