import os
import psycopg2

'''
This file is reponsible for initializing the Database Connection.
Setups all the required connections and creates tables
'''


def init():
    '''Set's up the connection'''
    connection_str = os.getenv('DATABASE_URL')
    connection = os.getenv(connection_str)
    return connection

meetups_tbl = '''CREATE TABLE IF NOT EXISTS meetup(
        id serial PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP NOT NULL,
        topic VARCHAR(80) NOT NULL,
        location VARCHAR(55) NOT NULL,
        images VARCHAR(80),
        tags VARCHAR(80),
        happeningOn TIMESTAMP NOT NULL
    );'''

users_tbl = '''CREATE TABLE IF NOT EXISTS usertbl (
        id serial PRIMARY KEY NOT NULL,
        firstname VARCHAR(55) NOT NULL,
        lastname VARCHAR(55) NOT NULL,
        username VARCHAR(55) NOT NULL,
        email VARCHAR(55) NOT NULL,
        password VARCHAR(100) NOT NULL,
        createOn TIMESTAMP NOT NULL,
        UNIQUE (email, username)
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
        title VARCHAR(80) NOT NULL,
        body VARCHAR(140) NOT NULL,
        votes INTEGER,
        CONSTRAINT ques_meetup_fk FOREIGN KEY (meetupid) REFERENCES meetup(id)
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
