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
            "images": ['http://lop.png', 'http://zip.png', 'http://zofgo.jpg', 'http://zik.jpg']
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

    def test_create_meetup_dateformat(self):
        '''Test the date format'''
        self.meetup['happeningOn'] = '20/15/2018'
        response = self.client.post('api/v2/meetups',
                                    data=json.dumps(self.meetup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("datetime format expected is yyyy-mm-dd",
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
        self.assertEqual("unexpected 'images' is a required property",
                         data['error'])

    def test_create_meetup_images_emptyarr(self):
        '''Test validation for empty array'''
        self.images['images'] = []
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected [] is too short", data['error'])

    def test_create_meetup_images_largearr(self):
        '''Test if images list is too large'''
        self.images['images'].append("http://trial.png")
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("""unexpected ['http://lop.png', 'http://zip.png', 'http://zofgo.jpg', 'http://zik.jpg', 'http://trial.png'] is too long""", data['error'])

    def test_create_meetup_images_arrtype(self):
        '''Test type of array'''
        self.images['images'] = ['lol', 0, "ol["]
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("images should be in uri format(http://img.png)",
                         data['error'])

    def tearDown(self):
        queries = delete_test()
        exec_queries(queries)
