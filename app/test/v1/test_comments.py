import json
import unittest

from app import create_app
from ...api.v1.models.basemodel import comments, questions


class CommentTestCase(unittest.TestCase):
    '''Tests the Comments Endpoints'''
    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()

        self.comment = {
            'userid': 1,
            'body': "I don't know where the event is could" +
                    " you please share the location"
        }

        comments.append({
            'id': 1,
            'time': '2019-01-15 08:43:30.571696',
            'userid': 1,
            'questionid': 1,
            'body': "Will there be food?"
        })

        questions.append({
            'id': 1,
            'userid': 1,
            'meetupid': 2,
            'title': 'Will there be food',
            'body': 'I will only attend if there is food',
            'votes': 15
        })

    def test_create_comment(self):
        '''Test create comment'''
        response = self.client.post('/api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn(" you please share the location", data['data']['body'])

    def test_create_comment_validation(self):
        '''Test comment object types match schema'''
        self.comment['userid'] = '1'
        response = self.client.post('api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected '1' is not of type 'number'",
                         data['message'])

    def test_create_comment_missing_object(self):
        '''Test comment json missing object'''
        del self.comment['userid']
        response = self.client.post('api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'userid' is a required property",
                         data['message'])

    def test_create_comment_badrequest(self):
        '''Test create comment with empty json'''
        response = self.client.post('api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/xml')
        self.assertEqual(response._status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected None is not of type 'object'",
                         data['message'])

    def test_create_comment_notfound(self):
        '''Test Question not found'''
        response = self.client.post('api/v1/questions/0/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['message'])

    def test_get_comments(self):
        '''Test Get comments under a question'''
        response = self.client.get('/api/v1/questions/1/comments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list)

    def test_get_comments_notfound(self):
        '''Test Get comments, not found question'''
        response = self.client.get('/api/v1/questions/0/comments')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['message'])

    def tearDown(self):
        comments.pop()
        questions.pop()
