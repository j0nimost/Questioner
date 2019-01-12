from .basemodel import BaseModel, questions


class Questions(BaseModel):
    '''Questions Model handles the business logic for the questions'''
    def __init__(self):
        super().__init__('questiondb')

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
        self.save(question)

    def update_votes(self, id: int, votes: int):
        '''
         Updates a question by providing votes, expects a question object
        '''
        _, question = self.find(id)
        question['votes'] += votes
        return question
