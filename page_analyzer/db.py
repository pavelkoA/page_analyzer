import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_url(url):
    query_arg = "id"
    if isinstance(url, str):
        query_arg = "name"
    query = f"""SELECT *
                FROM urls
                WHERE {query_arg} = %s"""
    data = [url]
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, data)
            data = cursor.fetchone()
    connect.close()
    return data


def read_checks(id):
    query = """SELECT *
               FROM url_checks
               WHERE url_id = %s
               ORDER BY id DESC"""
    data = [id]
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, data)
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


def write_url_checks(url):
    query = """INSERT INTO url_checks
               (url_id, status_code, h1, title, description)
               VALUES (%s, %s, %s, %s, %s)"""
    data = [url.get("url_id", ""),
            url.get("status_code", ""),
            url.get("h1", ""),
            url.get("title", ""),
            url.get("description", "")]
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(query, data)
    connect.close()


def write_url(url):
    query = "INSERT INTO urls (name) VALUES (%s)"
    data = [url]
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(query, data)
    connect.close()
