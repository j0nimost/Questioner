import datetime


meetups = []


class Meetups(object):
    '''Meetup model handles the business logic for the meetups'''
    id = len(meetups)+1
    createdOn = str(datetime.date.today())

    def __init__(self):
        pass

    @classmethod
    def create_meetup(self, location: str, images: list, topic: str,
                      happeningOn: str, tags: list):
        '''creates meetup'''
        meetup = {
            'id': self.id,
            'createdOn': self.createdOn,
            'topic': topic,
            'location': location,
            'images': images,
            'happeningOn': happeningOn,
            'tags': tags
        }
        meetups.append(meetup)
        return meetup

    @classmethod
    def find(self, id):
        if iter(meetups):
            for meetup in meetups:
                if meetup['id'] == id:
                    return meetup
            return None
