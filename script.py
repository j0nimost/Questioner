#!/usr/bin/env bash.
import os
from app.db import create_query, exec_queries, seed


def create():
    
    print("\n\t===============>")
    print("\n\t Create Script ")
    print("\n\t<================")
    
    try:
        os.system("""sudo psql -c "CREATE USER questioner WITH
                PASSWORD 'andela1';" -U questioner""")
        print("## user created")
        os.system("""sudo psql -c 'CREATE DATABASE qtest;' -U questioner""")
        print("### database created")
        os.system("""sudo psql -c "GRANT ALL privileges on database
                 qtest to questioner;" -U questioner""")
        print("#### connection complete")
        print("\n\n")
        # os.system("""sudo -u questioner PGPASSWORD=andela1 psql qtest""")
        os.system("psql PGPASSWORD=andela1 -U questioner -d qtest -a -f db.sql")
        # queries = create_query()
        ''' for q in queries:
                os.system(
                        "sudo psql -c qtest " + """{}""".format(q)
                        + " -U questioner"
                        )
        '''
        # exec_queries(queries)
        print("\nsuccessfully created tables")
        os.system("\dt")
        seed()
        print("\ndata seed")
    except Exception as e:
        print("\nAn error occured")
        print(e)

if __name__ == "__main__":
    create()