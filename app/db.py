import os
import psycopg2
import datetime

'''
This file is reponsible for initializing the Database Connection.
Setups all the required connections and creates tables
'''


def init():
    '''Set's up the connection'''
    x = os.getenv('FLASK_ENV')

    if x == 'testing':
        testing_db = os.getenv('DATABASE_URL_TEST')
        connection = psycopg2.connect(testing_db)
    else:
        prod_db = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(prod_db)
    return connection


def exec_queries(queries_: list):
    '''Create the tables for testdb'''
    db = init()
    db.autocommit = True
    try:
        for query in queries_:
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            cur.close()
    except Exception as e:
        return e
    finally:
        db.commit()
        cur.close()


def delete_test():
    '''Drop tables'''
    usertbl = "DROP TABLE IF EXISTS usertbl CASCADE;"
    meetuptbl = "DROP TABLE IF EXISTS meetup CASCADE;"
    commenttbl = "DROP TABLE IF EXISTS comment CASCADE;"
    questiontbl = "DROP TABLE IF EXISTS question CASCADE;"
    rsvptbl = "DROP TABLE IF EXISTS rsvp CASCADE;"
    roletbl = "DROP TABLE IF EXISTS roles CASCADE;"

    drop_queries = [usertbl, meetuptbl, roletbl, questiontbl,
                    commenttbl, rsvptbl]
    return drop_queries


def create_query():
    '''Create Queries'''
    meetups_tbl = '''CREATE TABLE IF NOT EXISTS meetup(
        id serial PRIMARY KEY NOT NULL,
        userid INTEGER,
        createdOn TIMESTAMP NOT NULL,
        topic VARCHAR(80) NOT NULL,
        location VARCHAR(55) NOT NULL,
        images TEXT[],
        tags TEXT[],
        happeningOn TIMESTAMP NOT NULL,
        CONSTRAINT userid_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE,
        UNIQUE(topic)
    );'''

    users_tbl = '''CREATE TABLE IF NOT EXISTS usertbl (
        id serial PRIMARY KEY NOT NULL,
        firstname VARCHAR(55) NOT NULL,
        lastname VARCHAR(55) NOT NULL,
        username VARCHAR(55) NOT NULL,
        email VARCHAR(55) NOT NULL,
        password VARCHAR(100) NOT NULL,
        userrole VARCHAR(20) NOT NULL,
        createOn TIMESTAMP NOT NULL,
        UNIQUE (email, username),
        CONSTRAINT role_fk FOREIGN KEY (userrole) REFERENCES roles(role)
    );'''

    comments_tbl = '''CREATE TABLE IF NOT EXISTS comment(
        id serial PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP NOT NULL,
        userid INTEGER NOT NULL,
        questionid INTEGER NOT NULL,
        body VARCHAR(140) NOT NULL,
        CONSTRAINT userid_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE,
        CONSTRAINT comment_question_fk FOREIGN KEY (questionid) REFERENCES
         question(id) ON DELETE CASCADE
    );'''

    question_tbl = '''CREATE TABLE IF NOT EXISTS question(
        id serial PRIMARY KEY NOT NULL,
        meetupid INTEGER NOT NULL,
        userid INTEGER NOT NULL,
        title VARCHAR(80) NOT NULL,
        body VARCHAR(140) NOT NULL,
        votes INTEGER,
        CONSTRAINT ques_meetup_fk FOREIGN KEY (meetupid) REFERENCES meetup(id)
        ON DELETE CASCADE,
        CONSTRAINT userid_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE
    );'''

    rsvp_tbl = '''CREATE TABLE IF NOT EXISTS rsvp(
        id serial PRIMARY KEY NOT NULL,
        userid INTEGER NOT NULL,
        meetupid INTEGER NOT NULL,
        isScheduled BOOLEAN NOT NULL,
        CONSTRAINT rsvp_meetup_fk FOREIGN KEY (meetupid) REFERENCES meetup(id)
        ON DELETE CASCADE,
        CONSTRAINT rsvp_user_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE
    );'''

    roles_tbl = '''CREATE TABLE IF NOT EXISTS roles(
        id serial NOT NULL,
        role VARCHAR(20) NOT NULL,
        CONSTRAINT roles_pk PRIMARY KEY (id, role),
        UNIQUE (role)
    );'''

    queries = [users_tbl, meetups_tbl, roles_tbl,
               question_tbl, comments_tbl, rsvp_tbl]
    return queries


def seed():
    creationTime = datetime.datetime.now()
    meetup = '''
        INSERT INTO meetup(createdOn, topic, location, happeningOn)
        Values('{}','Nairobi Go', 'Senteru Plaza', '2019-01-26')
        RETURNING id;
                '''.format(creationTime)

    roles = '''
        INSERT INTO roles(role) VALUES('admin');
        INSERT INTO roles(role) VALUES('user')
            '''

    queries = [meetup, roles]
    db = init()
    cur = db.cursor()

    try:
        for query in queries:
            cur.execute(query)
            id_ = cur.fetchone()[0]
            return id_
    except Exception as e:
        return e
    finally:
        cur.close()
