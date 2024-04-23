import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def read_url_by_name(url):
    query = """SELECT *
               FROM urls
               WHERE name = %s"""
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, [url])
            data = cursor.fetchone()
    connect.close()
    return data


def read_url_by_id(id):
    query = """SELECT *
               FROM urls
               WHERE id = %s"""
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, [id])
            data = cursor.fetchone()
    connect.close()
    return data


def read_checks(id):
    query = """SELECT *
               FROM url_checks
               WHERE url_id = %s
               ORDER BY id DESC"""
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, [id])
            data = cursor.fetchall()
    connect.close()
    return data


def read_urls_and_last_checks():
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
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    connect.close()
    return data


def write_url_checks(url_id,
                     status_code,
                     h1,
                     title,
                     description):
    query = """INSERT INTO url_checks
               (url_id, status_code, h1, title, description)
               VALUES (%s, %s, %s, %s, %s)"""
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(query, [url_id,
                                   status_code,
                                   h1,
                                   title,
                                   description])
    connect.close()


def write_url(url):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s)",
                [url]
            )
    connect.close()
