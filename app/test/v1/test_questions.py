import unittest
import json

from app import create_app
from ...api.v1.models.questionmodel import Questions, questions


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
        question_downvote = questions[0]
        question_downvote['votes'] = -1
        response = self.client.patch('api/v1/questions/1/downvote',
                                     data=json.dumps(question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        self.assertEqual(14, data['data']['votes'])

    def tearDown(self):
        questions.pop()
