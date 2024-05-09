import psycopg2
from psycopg2.extras import NamedTupleCursor
from functools import wraps


def connect_db(database_url):
    return psycopg2.connect(database_url)


def close(connect):
    return connect.close()


def commit():
    def wrap(func):
        @wraps(func)
        def wrapper(connect, func_argument):
            return_cursor = func(connect, func_argument)
            connect.commit()
            return return_cursor
        return wrapper
    return wrap


def get_url(connect, url):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query_arg = "id"
        if isinstance(url, str):
            query_arg = "name"
        query = f"""SELECT *
                    FROM urls
                    WHERE {query_arg} = %s"""
        query_data = [url]
        cursor.execute(query, query_data)
        return cursor.fetchone()


def read_checks(connect, id):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = """SELECT *
                   FROM url_checks
                   WHERE url_id = %s
                   ORDER BY id DESC"""
        query_data = [id]
        cursor.execute(query, query_data)
        return cursor.fetchall()


def read_urls_and_last_checks(connect):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
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


@commit()
def write_url_checks(connect, url):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = """INSERT INTO url_checks
                   (url_id, status_code, h1, title, description)
                   VALUES (%s, %s, %s, %s, %s)"""
        query_data = [url.get("url_id", ""),
                      url.get("status_code", ""),
                      url.get("h1", ""),
                      url.get("title", ""),
                      url.get("description", "")]
        cursor.execute(query, query_data)


@commit()
def write_url(connect, url):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        query = "INSERT INTO urls (name) VALUES (%s) RETURNING id"
        query_data = [url]
        cursor.execute(query, query_data)
        return cursor.fetchone().id
