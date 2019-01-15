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

        self.question_downvote = {
            'votes': -1
        }

        self.question_upvote = {
            'votes': 1
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
        '''Test create question endpoint'''
        response = self.client.post('api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Will there be food', str(json.loads(response.data)))

    def test_create_question_badrequest(self):
        '''Test create question empty json object'''
        response = self.client.post('api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected None is not of type 'object'",
                         data['error'])

    def test_question_validation(self):
        '''Test whether type's expected match validation'''
        self.question['title'] = 1212
        response = self.client.post('/api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 1212 is not of type 'string'",
                         data['error'])

    def test_question_missing_object(self):
        '''Test whether an object is missing from the Json object'''
        del self.question['title']
        response = self.client.post('/api/v1/questions',
                                    data=json.dumps(self.question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'title' is a required property",
                         data['error'])

    def test_downvote(self):
        '''Test downvote a question'''
        response = self.client.patch('api/v1/questions/1/downvote',
                                     data=json.dumps(self.question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(14, data['data'][0]['votes'])

    def test_downvote_notfound(self):
        '''Test downvote a not found question'''
        response = self.client.patch('api/v1/questions/0/downvote',
                                     data=json.dumps(self.question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        print(data)
        self.assertEqual('Not Found', data['error'])

    def test_downvote_validation(self):
        '''Test downvote object type matches schema'''
        self.question_downvote['votes'] = '-1'
        response = self.client.patch('/api/v1/questions/1/downvote',
                                     data=json.dumps(self.question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected '-1' is not of type 'number'",
                         data['error'])

    def test_downvote_missing_object(self):
        '''Test downvote object missing object'''
        del self.question_downvote['votes']
        response = self.client.patch('api/v1/questions/1/downvote',
                                     data=json.dumps(self.question_downvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'votes' is a required property",
                         data['error'])

    def test_upvote(self):
        '''Test upvote a question'''
        response = self.client.patch('api/v1/questions/1/upvote',
                                     data=json.dumps(self.question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(15, data['data'][0]['votes'])

    def test_upvote_notfound(self):
        '''Test upvote a question not found'''
        response = self.client.patch('api/v1/questions/0/upvote',
                                     data=json.dumps(self.question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['error'])

    def test_upvote_validation(self):
        '''Test upvote object types match schema'''
        self.question_upvote['votes'] = '1'
        response = self.client.patch('/api/v1/questions/1/upvote',
                                     data=json.dumps(self.question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected '1' is not of type 'number'",
                         data['error'])

    def test_upvote_missing_object(self):
        '''Test upvote object missing object'''
        del self.question_upvote['votes']
        response = self.client.patch('/api/v1/questions/1/upvote',
                                     data=json.dumps(self.question_upvote),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'votes' is a required property",
                         data['error'])

    def tearDown(self):
        questions.pop()
