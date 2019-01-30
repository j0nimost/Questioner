import os
from app.db import create_query, exec_queries, seed


def create():
    
    print("\n\t===============>")
    print("\n\t Create Script ")
    print("\n\t<================")
    
    try:
        os.system("""psql -c "CREATE USER questioner WITH
                PASSWORD 'andela1';" -U postgres""")
        print("## user created")
        os.system("""psql -c 'CREATE DATABASE IF
                NOT EXISTS qtest;' -U postgres""")
        print("### database created")
        os.system("""psql -c "GRANT ALL privileges on database
                 qtest to questioner;" -U postgres""")
        print("#### connection complete")

        queries = create_query()
        exec_queries(queries)
        print("\nsuccessfully created tables")
        seed()
        print("\ndata seed")
    except Exception as e:
        print("\nAn error occured")
        print(e)

if __name__ == "__main__":
    create()