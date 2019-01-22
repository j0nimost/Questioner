import os
import json
import unittest

from app import create_app
from ...db import exec_queries, create_query, delete_test


class AuthTestCase(unittest.TestCase):
    '''Test's Authorization and security'''
    def setUp(self):
        '''set up testing env'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        queries = create_query()
        self.val = exec_queries(queries)
        self.signup = {
            "fullname": "John Nyingi",
            "username": "j0nimost",
            "email": "j0ni@ke.com",
            "password": "**andela1",
            "confirmpassword": "**andela1"
        }

        self.signin = {
            "email": "j0ni@ke.com",
            "password": "**andela1"
        }

    def test_auth_signup(self):
        '''test signup'''
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual('j0nimost', data['data'][0]['user'][0]['username'])
        self.assertIsNotNone(data['data'][0]['token'])

    def test_auth_signup_password_match(self):
        '''Tests password matching'''
        self.signup['password'] = 'dfdfdfdpp'
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("password and confirm password don't match",
                         data['error'])

    def test_auth_signup_emailregex(self):
        '''Tests regex structure'''
        self.signup['email'] = 'joni.com'
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("email format expected is joe@lin.com",
                         data['error'])
                
    def test_auth_signup_fullnameregex(self):
        '''Test the fullname regex pattern'''
        self.signup['fullname'] = "mathogothanio"
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("fullname format should be 'John Doe'", data['error'])

    def test_auth_signup_password_length(self):
        '''Test password minimum length'''
        self.signup['password'] = 'lolpo'
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected password too short", data['error'])

    def test_auth_signup_mismatch(self):
        '''Test object types match schema'''
        self.signup['fullname'] = 20
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 20 is not of type 'string'",
                         data['error'])

    def test_auth_signup_missing(self):
        '''Test object schema doesnt miss required object'''
        del self.signup['fullname']
        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'fullname' is a required property",
                         data['error'])

    def test_auth_signup_conflict(self):
        ''''Tests if a user already exists'''
        _ = self.client.post('api/v2/auth/signup',
                             data=json.dumps(self.signup),
                             headers={
                                    "Content-Type": "application/json"})

        response = self.client.post('api/v2/auth/signup',
                                    data=json.dumps(self.signup),
                                    headers={
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual("user already exists with similar email/username",
                         data['error'])

    def test_auth_signin_wronginput(self):
        '''Test invalid email/password'''
        self.signin['email'] = 'kenn@gmail.com'
        response = self.client.post('api/v2/auth/signin',
                                    data=json.dumps(self.signin),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual('Wrong password/email', data['error'])

    def test_auth_signin_missingobject(self):
        '''Test if Signin object is missing an object'''
        del self.signin['email']
        response = self.client.post('api/v2/auth/signin',
                                    data=json.dumps(self.signin),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 'email' is a required property",
                         data['error'])

    def test_auth_signin_emailregex(self):
        self.signin['email'] = 'oktrythis.com'
        response = self.client.post('api/v2/auth/signin',
                                    data=json.dumps(self.signin),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("email format expected is joe@lin.com",
                         data['error'])

    def test_auth_signin_mismatch(self):
        '''Test if object types match schema'''
        self.signin['email'] = 25
        response = self.client.post('api/v2/auth/signin',
                                    data=json.dumps(self.signin),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual("unexpected 25 is not of type 'string'",
                         data['error'])

    def tearDown(self):
        dqueries = delete_test()
        exec_queries(dqueries)
