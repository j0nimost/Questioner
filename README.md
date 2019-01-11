## Questioner
This is Andela's Bootcamp Challenge one. The challenge is to create a UI based questioner web application as defined in [gh-pages](https://github.com/j0nimost/Questioner/tree/gh-pages). Using only Html, CSS and JavaScript. 

The Challenge two, will require the creation of an API. The API will consist of Endpoints defined in [develop branch](https://github.com/j0nimost/Questioner/tree/develop). The tools used for making the API include; Flask and Python 3.6, 

### Summary
The Questioner web app will allow a user to view Meetups and also schedule to attend them. Further more a user can create a question under a meetup and other users can vote on the question hence giving it more priority. A user can also comment on a question asked.

### Features
- A user should be able to sign up
- A user should be able to login
- A user should be able to post a question
- A user should be able to Upvote or Downvote a question
- A user should be able to comment on a question
- A user should have a profile
- A user should view top questions from their profile
- A user should view asked questions from their profile
- A user should view commented questions from their profile
- An Admin should be able to create a Meetup
- An Admin should be able to delete a Meetup
- A user should view Meetups

### Pivotal Tracker
[This](https://www.pivotaltracker.com/n/projects/2235178) is the link to Pivotal tracker stories. Under the Tag `ui/ux` and/or `design` for Challenge one; `api` label for Challenge two.

### Testing
#### Challenge One
- To access the Challenge one test access [gh-pages](https://j0nimost.github.io/Questioner/)

#### Challenge Two
- To test the API endpoints for challenge two access [heroku](https://questioneradc36.herokuapp.com/)

### Contributions
There are some standards as defined by Andela that are to be met especially in 
naming branches and commits; the following are some of the standards expected by 
Andela.

#### Branches 
- Features:
    `ft-<pivotal-story-id>-description`

- Chores:
    `ch-<pivotal-story-id>-description`

- Bugs:
    `bg-<pivotal-story-id>`

#### Commits
Commits naming will follow the branch naming structure except for the 
first and last commits which are expected to be named as;
- `git commit -m "start-<pivotal-story-id> message"`
- `git commit -m "finishes-<pivotal-story-id> message"`

#### Pull Requests
Andela's style of naming Pull requests require the prefix to be the `pivotal-story-id`; Hence it takes up the structure;
- `#213131613 Ch/Bg/Ft User can login` the Ch stands for Chore, Bg stands for Bug
    and Ft stands for Feature

#### Pull Request Description
There is an expected way of describing a pull requests that meets Andela's standards
for a `Feature` or `Chore` the following structure is expected;
```
## What does this PR do?


### Description of the Task to be completed


### Any background Tasks?


### Testing


### Screenshots
```

For a Bug the following Description structure is expected:
```
## What does this PR do?


### Expected


### Actual
```

### Author
John Nyingi
