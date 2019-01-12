import unittest
import json

from app import create_app
from ...api.v1.models.questionmodel import Questions
from ...api.v1.models.basemodel import questions


class MeetupsTestCase(unittest.TestCase):
    '''These are the test cases for question features'''
    def setUp(self):
        self.app = create_app(config='development')
        self.client = self.app.test_client()

        self.question = {
            'userid': 1,
            'meetupid': 2,
            'title': 'Will there be food',
            'body': 'I will only attend if there is food'
        }

        questions.append({
            'id': 1,
            'userid': 1,
            'meetupid': 2,
            'title': 'Will there be food',
            'body': 'I will only attend if there is food',
            'votes': 15
        })

    def test_create_question(self):
        response = self.client.post('api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Will there be food', str(json.loads(response.data)))

    def test_create_question_badrequest(self):
        response = self.client.post('api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid request type', str(json.loads(response.data)))

    def test_downvote(self):
        question_downvote = {
            'votes': -1
        }
        response = self.client.patch('api/v1/questions/1/downvote',
                                     data=json.dumps(question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(14, data['data'][0]['votes'])

    def test_downvote_notfound(self):
        question_downvote = {
            'votes': -1
        }
        response = self.client.patch('api/v1/questions/0/downvote',
                                     data=json.dumps(question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        print(data)
        self.assertEqual('Not Found', data['message'])

    def test_upvote(self):
        question_upvote = {
            'votes': 1
        }
        response = self.client.patch('api/v1/questions/1/upvote',
                                     data=json.dumps(question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(15, data['data'][0]['votes'])

    def test_upvote_notfound(self):
        question_upvote = {
            'votes': 1
        }
        response = self.client.patch('api/v1/questions/0/upvote',
                                     data=json.dumps(question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        print(data)
        self.assertEqual('Not Found', data['message'])

    def tearDown(self):
        questions.pop()
