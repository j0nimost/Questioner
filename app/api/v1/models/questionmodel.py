from .meetupmodel import Meetups

questions = []


class Questions(Meetups):
    '''Questions Model handles the business logic for the questions'''

    def __init__(self):
        super().__init__(self)

    @classmethod
    def create_question(self, userid: int, meetupid: int, title: str,
                        body: str):
        '''creates questions about a meetup'''
        question = {
            'userid': userid,
            'meetupid': meetupid,
            'title': title,
            'body': body
        }
        questions.append(question)
        return question
