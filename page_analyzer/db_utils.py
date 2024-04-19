import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_url_from_base_urls(data):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM urls
                    WHERE name = '{data}'"""
            )
            return cursor.fetchone()


def get_url_from_base_urls_by_id(id):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM urls
                    WHERE id = '{id}'"""
            )
            return cursor.fetchone()


def write_data_to_base_urls(data):
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            if not get_url_from_base_urls(data):
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s)",
                    [data]
                )
            return get_url_from_base_urls(data)


def get_all_urls_from_base_ulrs():
    with psycopg2.connect(DATABASE_URL) as connect:
        with connect.cursor() as cursor:
            cursor.execute("""SELECT *
                            FROM urls
                            ORDER BY id DESC""")
            return cursor.fetchall()
