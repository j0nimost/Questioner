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
            'id': len(questions)+1,
            'userid': userid,
            'meetupid': meetupid,
            'title': title,
            'body': body,
            'votes': 0
        }
        questions.append(question)
        return question

    @classmethod
    def find(self, id):
        '''Finds a specific question and returns a tuple'''
        if iter(questions):
            for index, question in enumerate(questions):
                if question['id'] == id:
                    return index, question
        return None, None

    @classmethod
    def update(self, question_update):
        '''Updates a question by providing votes, expects a question object'''
        index, question = self.find(question_update['id'])
        question['votes'] += question_update['votes']
        questions[index] = question
        return question
