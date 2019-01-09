import datetime


meetups = []


class Meetups(object):
    '''Meetup model handles the business logic for the meetups'''
    id = 0
    createdOn = None
    location = ''
    images = []
    topic = ''
    happeningOn = ''
    tags = []

    def __init__(self):
        self.id = len(meetups+1)
        self.createdOn = str(datetime.date.today())

    @classmethod
    def create_meetup(self):
        meetup = {
            'id': self.id,
            'createdOn': self.createdOn,
            'location': self.location,
            'images': self.images,
            'topic': self.topic,
            'happeningOn': self.happeningOn,
            'tags': self.tags
        }
        meetups.append(meetup)
        return meetup
