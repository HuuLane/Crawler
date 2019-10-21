import sqlite3
import logging
log = logging.getLogger('root')


def create_movies_table(conn):
    # 注意 CREATE TABLE 这种语句不分大小写
    sql_create = '''
    CREATE TABLE `movies` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `title`	TEXT NOT NULL ,
        `actors`	TEXT NOT NULL,
        `release`	TEXT,
        `score` REAL
    )
    '''
    try:
        conn.execute(sql_create)
        log.info('create movies table successfully!')
    except sqlite3.OperationalError as e:
        log.info('table `movies` already exists')


def insert(conn, title, actors, release, score):
    sql_insert = '''
    INSERT INTO
        movies(title,actors,release,score)
    VALUES
        (?, ?, ?, ?);
    '''
    conn.execute(sql_insert, (title, actors, release, score))
    log.info(f'insert {title} {actors}.. into movies table')


def show(conn):
    sql = '''
    SELECT
        title,actors,release,score
    FROM
        movies
    '''
    cursor = conn.execute(sql)
    log.info('result:', list(cursor))
    return


def conn_db(db_path='maoyan.sqlite'):
    conn = sqlite3.connect(db_path)
    log.info('conn to the maoyan.sqlite')
    return conn
