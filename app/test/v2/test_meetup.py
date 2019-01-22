import unittest
import json

from app import create_app
from ...db import create_query, delete_test, exec_queries, seed_meetup


class MeetupTestCase(unittest.TestCase):
    '''Test meetup'''
    def setUp(self):
        '''setup tests'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        queries = create_query()
        exec_queries(queries)

        self.meetup = {
            "topic": "Nairobi Golang",
            "location": "Senteru plaza",
            "happeningOn": "2019-01-26"
        }

        self.images = {
            "images": ['lop.png', 'zip.png']
        }

    def test_create_meetup(self):
        '''Test creation of meetup'''
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual('Nairobi Golang', data['data'][0]['topic'])

    def test_create_meetup_mismatch(self):
        '''Test if meetup object type matches schema'''
        self.meetup['topic'] = 20
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 20 is not of type 'string'",
                         data['error'])

    def test_create_meetup_missing(self):
        '''Test if meetup object is missing'''
        del self.meetup['happeningOn']
        response = self.client.post('api/v2/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'happeningOn' is a required property",
                         data['error'])

    def test_create_meetup_images_notfound(self):
        '''Test image insertion'''
        # Get seed
        response = self.client.patch("api/v2/meetups/0/images",
                                     data=json.dumps(self.images),
                                     content_type='application/json')
        # print(response.data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual("Not Found", data['error'])

    def test_create_meetup_images_missing(self):
        '''Test missing image object'''
        del self.images['images']
        response = self.client.patch("api/v2/meetups/1/images",
                                     data=json.dumps(self.images),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'images' is a required property", data['error'])

    def tearDown(self):
        queries = delete_test()
        exec_queries(queries)
