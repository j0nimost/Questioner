'''Define globally accessible lists to store data'''
meetups = []
questions = []
rsvps = []


class BaseModel(object):
    '''This is the base class and will be the Parent class'''
    def __init__(self, db=''):
        '''Initializes db type'''
        self.db = db

    def save(self, data={}):
        '''saves data to db'''
        db_add = self.check_db()
        self.data = data
        db_add.append(data)

    def check_db(self):
        '''Select a specified db type'''
        db_obj = dbconfig[self.db]
        return db_obj

    def return_data(self):
        '''returns data that has been added successfully to the db'''
        if self.save:
            return self.data
        return None

    def find(self, id: int):
        '''Generic find method returns tuple with index and item'''
        db_type = self.check_db()

        for index, item in enumerate(db_type):
            if id == item['id']:
                return index, item
        return None, None

    def update(self, data_update={}):
        '''Update existing data'''
        db = self.check_db()
        index, item = self.find(data_update['id'])
        if item:
            data = db[index]
            data.update(data_update)
            return data

    def delete(self, index: int):
        '''Delete existing data'''
        db = self.check_db()

        if index and isinstance(db, list):
            del db[index]
            return True
        return False

dbconfig = {
    'meetupsdb': meetups,
    'questiondb': questions,
    'rsvpsdb': rsvps
}
