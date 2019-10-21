import log
import maoyan
logger = log.setup_custom_logger('root')


def main():
    import db
    db_path = 'maoyan.sqlite'
    conn = db.conn_db(db_path)
    # create the table
    db.create_movies_table(conn)
    #
    movies = maoyan.get_movies()
    for m in movies:
        db.insert(conn, **m.__dict__)
    db.show(conn)
    conn.commit()
    conn.close()


def test():
    movies = maoyan.get_movies()
    for m in movies:
        print(m.__dict__)


if __name__ == "__main__":
    # test()
    main()
