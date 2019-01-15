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
                         data['error'])

    def test_create_comment_missing_object(self):
        '''Test comment json missing object'''
        del self.comment['userid']
        response = self.client.post('api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'userid' is a required property",
                         data['error'])

    def test_create_comment_badrequest(self):
        '''Test create comment with empty json'''
        response = self.client.post('api/v1/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/xml')
        self.assertEqual(response._status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected None is not of type 'object'",
                         data['error'])

    def test_create_comment_notfound(self):
        '''Test Question not found'''
        response = self.client.post('api/v1/questions/0/comments',
                                    data=json.dumps(self.comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['error'])

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
        self.assertEqual('Not Found', data['error'])

    def test_update_comments(self):
        '''Test update comments'''
        comment = comments[0]
        comment['body'] = 'It has been rescheduled to a later date'
        response = self.client.patch('/api/v1/comments/1',
                                     data=json.dumps(comment),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        self.assertEqual('It has been rescheduled to a later date',
                         data['data']['body'])

    def test_update_comments_validation(self):
        '''Test update objects type match schema'''
        comment = comments[0]
        comment['body'] = 20
        response = self.client.patch('/api/v1/comments/1',
                                     data=json.dumps(comment),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 20 is not of type 'string'",
                         data['error'])

    def test_update_comments_missing_object(self):
        '''Test update object, missing json object'''
        comment = comments[0]
        del comment['body']
        response = self.client.patch('/api/v1/comments/1',
                                     data=json.dumps(comment),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'body' is a required property",
                         data['error'])

    def test_update_comments_badrequest(self):
        '''Test comment update, comment not found'''
        comment = comments[0]
        response = self.client.patch('/api/v1/comments/1',
                                     data=json.dumps(comment),
                                     content_type='application/xml')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected None is not of type 'object'",
                         data['error'])

    def tearDown(self):
        comments.pop()
        questions.pop()
