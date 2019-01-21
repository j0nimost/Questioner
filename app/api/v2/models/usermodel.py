import datetime

from .basemodel import BaseModel


class UserModel(BaseModel):
    '''
    User Model class handles the business logic
    for user register and login
    '''
    def __init__(self):
        '''Initialize database connection'''
        super().__init__('usertbl')

    def name(self, fullname):
        '''Initialize firstname, lastname'''
        firstname, lastname = fullname.split(' ')
        return firstname, lastname

    def insert_query(self, fullname, username, email, password=''):
        '''query to save user the database'''
        firstname, lastname = self.name(fullname)
        user_obj = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': password,
            'createOn': datetime.date.today().__str__()
        }
        query = '''
                INSERT INTO {} (firstname, lastname, username, email,
                password, createOn)
                VALUES (%(firstname)s, %(lastname)s, %(username)s,
                %(email)s, %(password)s, %(createOn)s) ON CONFLICT
                (email,username) DO NOTHING RETURNING id;'''.format(self.table)

        id_ = super().insert(user_obj, query)
        return id_

user_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "fullname": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string",
                  "pattern": r"""(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-
                                    .]+$)"""},
        "password": {"type": "string",
                     "minLength": 8},
        "confirmpassword": {"type": "string",
                            "minLength": 8}
    },
    "required": ["fullname", "username", "email",
                 "password", "confirmpassword"]
}

login_schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "email": {"type": "string",
                  "pattern": r"""(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-
                                    .]+$)"""},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]

}
