from app.db import create_query, exec_queries, seed


def create():
    print("\n\t===============>")
    print("\n\t Create Script ")
    print("\n\t<================")
    try:
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