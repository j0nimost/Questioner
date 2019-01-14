import unittest
import json

from app import create_app
from ...api.v1.models.basemodel import meetups


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

        self.rsvp = {
            'userid': 1
        }

    def test_create_meetup(self):
        '''Test create a meetup endpoint'''
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print('{} code'.format(response.status_code))
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_create_meetup_badrequest(self):
        '''Test create a meetup empty json object'''
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        self.assertIn("unexpected None is not of type 'object'",
                      str(json.loads(response.data)))

    def test_meetup_validation(self):
        '''Test meetup object types match to schema'''
        self.meetup['topic'] = 21
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 21 is not of type 'string'",
                         data['message'])

    def test_meetup_missing_object(self):
        '''Test missing object from meetup json object'''
        '''this tests if an object is missing in json request'''
        del self.meetup['topic']
        response = self.client.post('/api/v1/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'topic' is a required property",
                         data['message'])

    def test_get_upcoming(self):
        '''Test get meetups'''
        response = self.client.get('/api/v1/meetups/upcoming')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_get_meetup(self):
        '''Test get a single meetup'''
        response = self.client.get('/api/v1/meetups/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nairobi Go Meetup', str(json.loads(response.data)))

    def test_get_meetup_notfound(self):
        '''Test get a meetup not found'''
        response = self.client.get('/api/v1/meetups/0')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not Found', str(json.loads(response.data)))

    def test_create_rsvp(self):
        '''Test create rsvp'''
        pass

    def test_create_rsvp_badrequest(self):
        '''Test create rsvp empty rsvp json object'''
        response = self.client.post('/api/v1/meetups/1/rsvps',
                                    data=json.dumps(self.rsvp),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected None is not of type 'object'",
                         data['message'])

    def test_create_rsvp_notfound(self):
        '''Test create rsvp, meetup not found'''
        response = self.client.post('/api/v1/meetups/0/rsvps',
                                    data=json.dumps(self.rsvp),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['message'])

    def test_rsvp_validation(self):
        '''Test rsvp object types match schema'''
        self.rsvp['userid'] = '1'
        response = self.client.post('/api/v1/meetups/1/rsvps',
                                    data=json.dumps(self.rsvp),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected '1' is not of type 'number'",
                         data['message'])

    def test_rsvp_missing_object(self):
        '''Test rsvp json missing json object'''
        del self.rsvp['userid']
        response = self.client.post('/api/v1/meetups/1/rsvps',
                                    data=json.dumps(self.rsvp),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'userid' is a required property",
                         data['message'])

    def tearDown(self):
        meetups.pop()
