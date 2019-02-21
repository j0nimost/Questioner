import os
import psycopg2
import datetime

from flask import g, current_app
'''
This file is reponsible for initializing the Database Connection.
Setups all the required connections and creates tables
'''
testdb = os.getenv('DATABASE_URL_TEST')
devdb = os.getenv('DATABASE_URL')


def get_db(env=None):
    '''Sets test db config'''

    if '_db' not in g:
        '''set the db for test env'''
        if env.islower == 'testing':
            g._db = psycopg2.connect(testdb)
        else:
            g._db = psycopg2.connect(devdb)
    return g._db


def close_conn(e=None):
    '''close connections'''
    _db = g.pop('_db', None)

    if _db is not None:
        _db.close()


def init_app(app):
    '''set up the tables'''
    app.teardown_appcontext(close_conn)
    create_tables()


def create_tables():
    db = get_db()

    with current_app.open_resource('db.sql') as query:
        cur = db.cursor()
        cur.execute(query.read())
        db.commit()


def drop_tables():
    db = get_db('testing')

    with current_app.open_resource('drop_tbl.sql') as query:
        cur = db.cursor()
        cur.execute(query.read())
        db.commit()
