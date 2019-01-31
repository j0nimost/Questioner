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
        if env == 'development':
            g._db = psycopg2.connect(devdb)
        else:
            g._db = psycopg2.connect(testdb)
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


'''def init(env=''):
    if env == 'testing':
        prod_db = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(prod_db)
        return connection
    else:
        testing_db = os.getenv('DATABASE_URL_TEST')
        connection = psycopg2.connect(testing_db)
        return connection



def exec_queries(queries_: list):
    try:
        for query in queries_:
            db = init()
            cur = db.cursor()
            cur.execute(query)
            print("vako")
            db.commit()
            cur.close()
            
    except Exception as e:
        pass
    finally:
        db.close()'''
