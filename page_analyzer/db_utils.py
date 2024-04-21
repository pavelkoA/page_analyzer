import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

from collections import namedtuple


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_url_from_base_urls(data):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM urls
                    WHERE name = '{data}'"""
            )
            data = cursor.fetchone()
    connect.close()
    return data


def get_url_from_base_urls_by_id(id):
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


def write_data_to_base_urls(data):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            if not get_url_from_base_urls(data):
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s)",
                    [data]
                )
    connect.close()
    return get_url_from_base_urls(data)


def get_all_urls_from_base_ulrs():
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("""SELECT *
                            FROM urls
                            ORDER BY id DESC""")
            data = cursor.fetchall()
    connect.close()
    return data


def write_new_check_from_url_checks(url_id,
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


def get_checks_from_url_checks(id):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(f"""SELECT *
                               FROM url_checks
                               WHERE url_id = {id}
                               ORDER BY id DESC""")
            data = cursor.fetchall()
    connect.close()
    return data
