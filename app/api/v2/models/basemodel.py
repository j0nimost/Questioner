import os
from psycopg2.extras import RealDictCursor
from flask import current_app
from flask import app
from ....db import get_db

'''
This is the basemodel that will handle shared logic
'''


class BaseModel(object):
    '''Generic Base Model'''
    def __init__(self, table=''):
        '''Initialize Db connection'''
        self.table = table

    def insert(self, data: dict, query: str):
        '''abstract method to insert data'''
        dbconn = get_db(current_app.env)
        # dbconn.autocommit = True
        if dbconn:
            cur = dbconn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, data)
            if cur.rowcount != 0:
                id_ = cur.fetchone()['id']
                dbconn.commit()
                cur.close()
                return id_
            dbconn.commit()
            cur.close()
        return None

    def fetch(self, name, item):
        '''abstract method to fetch item'''
        dbconn = get_db(current_app.env)
        cur = dbconn.cursor(cursor_factory=RealDictCursor)
        query = '''
                    SELECT * FROM {} WHERE {}='{}'
                '''.format(self.table, name, item,)
        cur.execute(query)
        data = cur.fetchone()
        cur.close()
        return data

    def exists(self, name, item):
        '''checks if item exists'''
        dbconn = get_db(current_app.env)
        cur = dbconn.cursor()
        query = """
                SELECT EXISTS (SELECT * FROM {}
                 WHERE {}='{}');
                """.format(self.table, name, item)
        cur.execute(query)
        exists = cur.fetchone()[0]  # error
        cur.close()
        return exists

    def update(self, query, data):
        '''abstract method handles updates'''
        dbconn = get_db(current_app.env)
        cur = dbconn.cursor(cursor_factory=RealDictCursor)

        try:
            if isinstance(data, list):
                cur.executemany(query, data)
                dbconn.commit()
                cur.close()
                return True
            else:
                cur.execute(query, data)
                id_ = cur.fetchone()['id']
                dbconn.commit()
                cur.close()
                return id_
        except Exception as e:
            return e

    def delete(self):
        '''abstract method delete items'''
        pass
