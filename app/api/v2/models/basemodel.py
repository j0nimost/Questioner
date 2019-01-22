from ....db import init

'''
This is the basemodel that will handle shared logic
'''


class BaseModel(object):
    '''Generic Base Model'''
    def __init__(self, table=''):
        '''Initialize Db connection'''
        self.conn = init()
        self.table = table

    def insert(self, data: dict, query: str):
        '''abstract method to insert data'''
        dbconn = self.conn
        # dbconn.autocommit = True
        cur = dbconn.cursor()
        cur.execute(query, data)
        if cur.rowcount != 0:
            id_ = cur.fetchone()[0]
            cur.close()
            return id_
        cur.close()
        return None

    def fetch(self, name, item):
        '''abstract method to fetch item'''
        dbconn = self.conn
        cur = dbconn.cursor()
        query = '''
                    SELECT * FROM {} WHERE {}='{}'
                '''.format(self.table, name, item,)
        cur.execute(query)
        data = cur.fetchone()
        cur.close()
        return data

    def exists(self, name, item):
        '''checks if item exists'''
        dbconn = self.conn
        cur = dbconn.cursor()
        query = """
                SELECT EXISTS (SELECT * FROM {}
                 WHERE {}='{}');
                """.format(self.table, name, item)
        cur.execute(query)
        exists = cur.fetchone()[0]
        cur.close()
        return exists

    def save(self, conn: init()):
        '''abstract handles closing of connections'''
        conn.commit()
        conn.cursor().close()
        return True

    def update(self, query, data):
        '''abstract method handles updates'''
        dbconn = self.conn
        cur = dbconn.cursor()

        if isinstance(data, list):
            cur.executemany(query, data)
            id_ = cur.fetchone()[0]
            dbconn.commit()
            cur.close()
            return id_
        else:
            cur.execute(query, data)
            id_ = cur.fetchone()[0]
            dbconn.commit()
            cur.close()
            return id_

    def delete(self):
        '''abstract method delete items'''
        pass
