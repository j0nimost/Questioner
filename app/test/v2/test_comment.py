import os
import json
import unittest

from app import create_app
from ...db import get_db, drop_tables


class CommentTestCase(unittest.TestCase):
    '''Tests for the comment endpoint'''
    def setUp(self):
        env = os.getenv('TEST_SETTINGS')
        self.app = create_app(env)

        with self.app.app_context():
            get_db(env)
        self.client = self.app.test_client()

        self.meetup = {
            "topic": "Nairobi Golang",
            "location": "Senteru plaza",
            "happeningOn": "2019-01-26"
        }

        self.question = {
            "topic": "Where is the meetup",
            "body": "I would like to know the venue of the meetup"
        }

        signup = {
            "fullname": "John Nyingi",
            "username": "j0nimost",
            "email": "j0ni@ke.com",
            "password": "**andela1",
            "confirmpassword": "**andela1",
            "role": 'admin'
        }

        # Get token
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(signup),
                                    headers={
                                        "Content-Type": "application/json"})
        data = json.loads(response.data)
        self.token = data['data'][0]['token']

        self.auth_header = {
                            "Authorization": "bearer {}".format(self.token),
                            "Content-Type": "application/json"
                            }

        self.comment = {
            "body": "I think the meetup will be in Senteru plaza"
        }

    def test_create_comment(self):
        '''Test create comment'''
        meetup_resp = self.client.post('api/v2/meetups',
                                       data=json.dumps(self.meetup),
                                       headers=self.auth_header)
        self.assertEqual(meetup_resp.status_code, 201)
        meetup_data = json.loads(meetup_resp.data)
        meetupid = meetup_data['data'][0]['id']
        self.assertIsInstance(meetupid, int)
        ques_resp = self.client.post(
            '''api/v2/meetups/{}/questions'''.format(meetupid),
            data=json.dumps(self.question),
            headers=self.auth_header
            )
        self.assertEqual(ques_resp.status_code, 201)
        ques_data = json.loads(ques_resp.data)
        quesid = ques_data['data'][0]['id']
        self.assertIsInstance(quesid, int)

        comment_res = self.client.post(
            '''api/v2/questions/{}/comments'''.format(quesid),
            data=json.dumps(self.comment),
            headers=self.auth_header
            )
        self.assertEqual(comment_res.status_code, 201)
        comment_data = json.loads(comment_res.data)
        self.assertEqual('I think the meetup will be in Senteru plaza',
                         comment_data['data'][0]['body'])

    def test_create_comment_notfound(self):
        '''Test if question does not exist'''
        response = self.client.post('api/v2/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual('Not Found', data['error'])

    def test_create_comment_missingobj(self):
        '''Test missing object in schema'''
        self.comment['body'] = ''
        response = self.client.post('api/v2/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "unexpected pattern for body")

        del self.comment['body']
        response = self.client.post('api/v2/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'],
                         "unexpected 'body' is a required property")

    def test_create_comment_type_validation(self):
        '''Test type validation'''
        self.comment['body'] = 51
        response = self.client.post('api/v2/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['error'],
            "unexpected 51 is not of type 'string'")

    def test_create_comment_length_validation(self):
        '''Test comment length validation'''
        self.comment['body'] = """One of the most effective approach to better meetings is No Meeting without an Agenda.A few years ago, I worked for a customer where meetings were the answer for almost everything, but no one bothered writing down the questions. After a while, it got extremely annoying and our team started to decline every meeting request with no fixed agenda. From that point on, meetings got shorter and actually had an outcome. """
        response = self.client.post('api/v2/questions/1/comments',
                                    data=json.dumps(self.comment),
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['error'],
            "unexpected 'One of the most effective approach to better meetings is No Meeting without an Agenda.A few years ago, I worked for a customer where meetings were the answer for almost everything, but no one bothered writing down the questions. After a while, it got extremely annoying and our team started to decline every meeting request with no fixed agenda. From that point on, meetings got shorter and actually had an outcome. ' is too long"
            )

    def test_update_comment(self):
        '''Test the update comment'''
        meetup_resp = self.client.post('api/v2/meetups',
                                       data=json.dumps(self.meetup),
                                       headers=self.auth_header)
        self.assertEqual(meetup_resp.status_code, 201)
        meetup_data = json.loads(meetup_resp.data)
        meetupid = meetup_data['data'][0]['id']
        self.assertIsInstance(meetupid, int)
        ques_resp = self.client.post(
            '''api/v2/meetups/{}/questions'''.format(meetupid),
            data=json.dumps(self.question),
            headers=self.auth_header
            )
        self.assertEqual(ques_resp.status_code, 201)
        ques_data = json.loads(ques_resp.data)
        quesid = ques_data['data'][0]['id']
        self.assertIsInstance(quesid, int)

        comment_res = self.client.post(
            '''api/v2/questions/{}/comments'''.format(quesid),
            data=json.dumps(self.comment),
            headers=self.auth_header
            )
        self.assertEqual(comment_res.status_code, 201)
        comment_data = json.loads(comment_res.data)
        self.assertEqual('I think the meetup will be in Senteru plaza',
                         comment_data['data'][0]['body'])

        commentid = comment_data['data'][0]['id']
        self.comment['body'] = 'Where is the meeting point?'
        update_response = self.client.patch(
                        'api/v2/comments/{}'.format(commentid),
                        data=json.dumps(self.comment),
                        headers=self.auth_header)
        self.assertEqual(update_response.status_code, 202)
        update_data = json.loads(update_response.data)
        self.assertEqual('Where is the meeting point?',
                         update_data['data'][0]['body'])

    def test_update_comment_notfound(self):
        '''Test missing comment'''
        update_response = self.client.patch(
                        'api/v2/comments/0',
                        data=json.dumps(self.comment),
                        headers=self.auth_header)
        self.assertEqual(update_response.status_code, 404)
        update_data = json.loads(update_response.data)
        self.assertEqual('Not Found',
                         update_data['error'])

    def test_delete_comment(self):
        '''Test delete comment'''
        meetup_resp = self.client.post('api/v2/meetups',
                                       data=json.dumps(self.meetup),
                                       headers=self.auth_header)
        self.assertEqual(meetup_resp.status_code, 201)
        meetup_data = json.loads(meetup_resp.data)
        meetupid = meetup_data['data'][0]['id']
        self.assertIsInstance(meetupid, int)
        ques_resp = self.client.post(
            '''api/v2/meetups/{}/questions'''.format(meetupid),
            data=json.dumps(self.question),
            headers=self.auth_header
            )
        self.assertEqual(ques_resp.status_code, 201)
        ques_data = json.loads(ques_resp.data)
        quesid = ques_data['data'][0]['id']
        self.assertIsInstance(quesid, int)

        comment_res = self.client.post(
            '''api/v2/questions/{}/comments'''.format(quesid),
            data=json.dumps(self.comment),
            headers=self.auth_header
            )
        self.assertEqual(comment_res.status_code, 201)
        comment = json.loads(comment_res.data)
        commentid = comment['data'][0]['id']

        response = self.client.delete(
            'api/v2/comments/{}'.format(commentid),
            headers=self.auth_header
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_comment_notfound(self):
        '''Test not found comment'''
        response = self.client.delete(
            'api/v2/comments/0',
            headers=self.auth_header
        )
        self.assertEqual(response.status_code, 404)
        error = json.loads(response.data)
        self.assertEqual('Not Found', error['error'])

    def tearDown(self):
        with self.app.app_context():
            drop_tables()
