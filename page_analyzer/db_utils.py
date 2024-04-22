import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def read_url_by_name(url):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM urls
                    WHERE name = '{url}'"""
            )
            data = cursor.fetchone()
    connect.close()
    return data


def read_url_by_id(id):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM urls
                    WHERE id = '{id}'"""
            )
            data = cursor.fetchone()
    connect.close()
    return data


def read_checks(id):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(f"""SELECT *
                               FROM url_checks
                               WHERE url_id = {id}
                               ORDER BY id DESC""")
            data = cursor.fetchall()
    connect.close()
    return data


def read_urls_and_last_checks():
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("""select
                                urls.id as id,
                                urls.name as name,
                                url_checks.status_code as status_code,
                                url_checks.created_at as created_at
                              from urls
                              left join url_checks
                              on urls.id = url_checks.url_id
                              and url_checks.id = (select max(id)
                                    from url_checks
                                    where urls.id = url_checks.url_id)
                              order by urls.id desc;""")
            data = cursor.fetchall()
    connect.close()
    return data


def write_url_checks(url_id,
                     status_code,
                     h1,
                     title,
                     description):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                """INSERT INTO url_checks
                   (url_id, status_code, h1, title, description)
                   VALUES (%s, %s, %s, %s, %s)""",
                [url_id, status_code, h1, title, description])
    connect.close()


def write_url(url):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s)",
                [url]
            )
    connect.close()
