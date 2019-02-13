CREATE TABLE IF NOT EXISTS roles(
        id serial NOT NULL,
        role VARCHAR(20) NOT NULL,
        CONSTRAINT roles_pk PRIMARY KEY (id, role),
        UNIQUE (role)
    );

CREATE TABLE IF NOT EXISTS usertbl (
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
    );


CREATE TABLE IF NOT EXISTS meetup(
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
    );

CREATE TABLE IF NOT EXISTS question(
        id serial PRIMARY KEY NOT NULL,
        meetupid INTEGER NOT NULL,
        userid INTEGER NOT NULL,
        title VARCHAR(80) NOT NULL,
        body VARCHAR(140) NOT NULL,
        voteup INTEGER DEFAULT 0,
        votedown INTEGER DEFAULT 0,
        CONSTRAINT ques_meetup_fk FOREIGN KEY (meetupid) REFERENCES meetup(id)
        ON DELETE CASCADE,
        CONSTRAINT userid_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS voteup(
    id serial PRIMARY KEY NOT NULL,
    questionid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    CONSTRAINT voteup_question_fk FOREIGN KEY (questionid) REFERENCES question(id)
    ON DELETE CASCADE,
    CONSTRAINT voteup_user_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
    ON DELETE CASCADE,
    UNIQUE (questionid, userid)
    );

CREATE TABLE IF NOT EXISTS votedown(
    id serial PRIMARY KEY NOT NULL,
    questionid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    CONSTRAINT votedown_question_fk FOREIGN KEY (questionid) REFERENCES question(id)
    ON DELETE CASCADE,
    CONSTRAINT votedown_user_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
    ON DELETE CASCADE,
    UNIQUE (questionid, userid)
    );

CREATE TABLE IF NOT EXISTS comment(
        id serial PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP NOT NULL,
        userid INTEGER NOT NULL,
        questionid INTEGER NOT NULL,
        body VARCHAR(140) NOT NULL,
        CONSTRAINT userid_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
        ON DELETE CASCADE,
        CONSTRAINT comment_question_fk FOREIGN KEY (questionid) REFERENCES
         question(id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS rsvp(
    id serial PRIMARY KEY NOT NULL,
    userid INTEGER NOT NULL,
    meetupid INTEGER NOT NULL,
    CONSTRAINT rsvp_user_fk FOREIGN KEY (userid) REFERENCES usertbl(id)
    ON DELETE CASCADE,
    CONSTRAINT rsvp_meetup_fk FOREIGN KEY (meetupid) REFERENCES meetup(id)
    ON DELETE CASCADE,
    UNIQUE (userid, meetupid)
    );

INSERT INTO roles(role) VALUES('admin') ON CONFLICT DO NOTHING;
INSERT INTO roles(role) VALUES('user') ON CONFLICT DO NOTHING;