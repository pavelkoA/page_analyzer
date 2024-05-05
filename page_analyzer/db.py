import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
from functools import wraps


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def connect_db(database_url):
    def wrap(func):
        @wraps(func)
        def wrapper(func_argument=None):
            with psycopg2.connect(database_url) as connect:
                with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    if func_argument:
                        return_cursor = func(cursor, func_argument)
                    else:
                        return_cursor = func(cursor)
            connect.close()
            return return_cursor
        return wrapper
    return wrap


@connect_db(DATABASE_URL)
def get_url(cursor, url):
    query_arg = "id"
    if isinstance(url, str):
        query_arg = "name"
    query = f"""SELECT *
                FROM urls
                WHERE {query_arg} = %s"""
    query_data = [url]
    cursor.execute(query, query_data)
    return cursor.fetchone()


@connect_db(DATABASE_URL)
def read_checks(cursor, id):
    query = """SELECT *
               FROM url_checks
               WHERE url_id = %s
               ORDER BY id DESC"""
    query_data = [id]
    cursor.execute(query, query_data)
    return cursor.fetchall()


@connect_db(DATABASE_URL)
def read_urls_and_last_checks(cursor):
    query = """SELECT
                urls.id AS id,
                urls.name AS name,
                url_checks.status_code AS status_code,
                url_checks.created_at AS created_at
               FROM urls
               LEFT JOIN url_checks
               ON urls.id = url_checks.url_id
               AND url_checks.id = (SELECT max(id)
                FROM url_checks
                WHERE urls.id = url_checks.url_id)
               ORDER BY urls.id DESC;"""
    cursor.execute(query)
    return cursor.fetchall()


@connect_db(DATABASE_URL)
def write_url_checks(cursor, url):
    query = """INSERT INTO url_checks
               (url_id, status_code, h1, title, description)
               VALUES (%s, %s, %s, %s, %s)"""
    query_data = [url.get("url_id", ""),
                  url.get("status_code", ""),
                  url.get("h1", ""),
                  url.get("title", ""),
                  url.get("description", "")]
    cursor.execute(query, query_data)


@connect_db(DATABASE_URL)
def write_url(cursor, url):
    query = "INSERT INTO urls (name) VALUES (%s)"
    query_data = [url]
    cursor.execute(query, query_data)
