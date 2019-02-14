import os
import unittest
import json

from app import create_app
from ...db import get_db, drop_tables


class MeetupTestCase(unittest.TestCase):
    '''Test meetup'''
    def setUp(self):
        '''setup tests'''
        env = os.getenv('TEST_SETTINGS')
        self.app = create_app(env)

        with self.app.app_context():
            get_db(env)

        self.client = self.app.test_client()
        # signup a user to get token
        
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
        self.meetup = {
            "topic": "Nairobi Golang",
            "location": "Senteru plaza",
            "happeningOn": "2019-01-26"
        }

        self.question = {
            "topic": "Where is the meetup",
            "body": "I would like to know the venue of the meetup"
        }

        self.images = {
            "images": ['http://lop.png', 'http://zip.png', 'http://zofgo.jpg',
                       'http://zik.jpg']
        }

        self.tags = {
            "tags": ["tech", "theology", "art", "music"]
        }

        self.auth_header = {
                            "Authorization": "bearer {}".format(self.token),
                            "Content-Type": "application/json"
                            }

    def test_getall_meetups(self):
        '''Test get upcoming meetups'''
        response = self.client.get('api/v2/meetups/upcoming',
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list)

    def test_get_meetup(self):
        '''Test get single meetup with questions'''
        meetup_res = self.client.post("api/v2/meetups",
                                      data=json.dumps(self.meetup),
                                      headers=self.auth_header)
        self.assertEqual(meetup_res.status_code, 201)
        data_meetup = json.loads(meetup_res.data)
        meetupid = data_meetup['data'][0]['id']

        question_res = self.client.post(
            "api/v2/meetups/{}/questions".format(meetupid),
            data=json.dumps(self.question),
            headers=self.auth_header)
        self.assertEqual(question_res.status_code, 201)

        get_meetup = self.client.get(
            "api/v2/meetups/{}".format(meetupid),
            headers=self.auth_header)

        self.assertEqual(get_meetup.status_code, 200)
        meetup = json.loads(get_meetup.data)
        self.assertEqual(
            "Where is the meetup",
            meetup['data'][0]['questions'][0]['title']
        )

    def get_meetup_notfound(self):
        '''Test not found error'''
        response = self.client.get(
            "api/v2/meetups/0",
            headers=self.auth_header)

        self.assertEqual(response.status_code, 404)
        err = json.loads(response.data)
        self.assertEqual("Not Found", err['error'])

    def test_create_meetup(self):
        '''Test creation of meetup'''
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual('Nairobi Golang', data['data'][0]['topic'])
        self.id_meetup = data['data'][0]['id']

    def test_create_meetup_mismatch(self):
        '''Test if meetup object type matches schema'''
        self.meetup['topic'] = 20
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetup),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 20 is not of type 'string'",
                         data['error'])

    def test_create_meetup_missing(self):
        '''Test if meetup object is missing'''
        del self.meetup['happeningOn']
        response = self.client.post('api/v2/meetups',
                                    data=json.dumps(self.meetup),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'happeningOn' is a required property",
                         data['error'])

    def test_create_meetup_dateformat(self):
        '''Test the date format'''
        self.meetup['happeningOn'] = '20/15/2018'
        response = self.client.post('api/v2/meetups',
                                    data=json.dumps(self.meetup),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("datetime format expected is yyyy-mm-dd",
                         data['error'])

    def test_create_meetup_images(self):
        '''Test patch images to meetups'''
        meetup_res = self.client.post("api/v2/meetups",
                                      data=json.dumps(self.meetup),
                                      headers=self.auth_header)
        data = json.loads(meetup_res.data)
        id_ = data['data'][0]['id']
        response = self.client.patch("api/v2/meetups/{}/images".format(id_),
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 202)

    def test_create_meetup_images_notfound(self):
        '''Test image insertion'''
        response = self.client.patch("api/v2/meetups/0/images",
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual("Not Found", data['error'])

    def test_create_meetup_images_missing(self):
        '''Test missing image object'''
        del self.images['images']
        response = self.client.patch("api/v2/meetups/1/images",
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'images' is a required property",
                         data['error'])

    def test_create_meetup_images_emptyarr(self):
        '''Test validation for empty array'''
        self.images['images'] = []
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected [] is too short", data['error'])

    def test_create_meetup_images_largearr(self):
        '''Test if images list is too large'''
        self.images['images'].append("http://trial.png")
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("""unexpected ['http://lop.png', 'http://zip.png', 'http://zofgo.jpg', 'http://zik.jpg', 'http://trial.png'] is too long""", data['error'])

    def test_create_meetup_images_arrtype(self):
        '''Test type of array'''
        self.images['images'] = ['lol', 0, "ol["]
        response = self.client.patch('api/v2/meetups/1/images',
                                     data=json.dumps(self.images),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("images should be in uri format(http://img.png)",
                         data['error'])

    def test_create_meetup_tags(self):
        '''Test creation of tags'''
        meetup_res = self.client.post("api/v2/meetups",
                                      data=json.dumps(self.meetup),
                                      headers=self.auth_header)
        data = json.loads(meetup_res.data)
        id_ = data['data'][0]['id']
        response = self.client.patch('api/v2/meetups/{}/tags'.format(id_),
                                     data=json.dumps(self.tags),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 202)

    def test_create_meetup_tags_emptyarr(self):
        '''Test empty list'''
        self.tags['tags'] = []
        response = self.client.patch('api/v2/meetups/1/tags',
                                     data=json.dumps(self.tags),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertEqual(data['error'], "unexpected [] is too short")

    def test_create_meetup_tags_arrtype(self):
        '''Test object type'''
        self.tags['tags'] = [20, 'pop']
        response = self.client.patch('api/v2/meetups/1/tags',
                                     data=json.dumps(self.tags),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "unexpected 20 is not of type 'string'")

    def test_create_meetup_tags_largearr(self):
        '''Test tags arr limit'''
        self.tags['tags'].append('politics')
        response = self.client.patch('api/v2/meetups/1/tags',
                                     data=json.dumps(self.tags),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "unexpected ['tech', 'theology', 'art', 'music', 'politics'] is too long")

    def test_create_meetup_tags_notfound(self):
        '''Test meetup not found'''
        response = self.client.patch('api/v2/meetups/0/tags',
                                     data=json.dumps(self.tags),
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not Found')

    def tearDown(self):
        with self.app.app_context():
            drop_tables()
