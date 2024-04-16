import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for

from page_analyzer.validator import get_url, is_url


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_data_in_base_urls(connect, data):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT name
                FROM urls
                WHERE name = '{data}'"""
        )
        return cursor.fetchone()


def write_data_to_base_urls(connect, data):
    with connect.cursor() as cursor:
        base_data = get_data_in_base_urls(connect, data)
        if not base_data:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s)",
                [data]
            )
        else:
            raise
        connect.commit()
        return get_data_in_base_urls(connect, data)




app = Flask(__name__)
app.secret_key = "MySuperSecretKey"


@app.route("/")
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html",
                           messages=messages)


@app.post("/urls")
def create_url():
    site = request.form.get("url")
    if not is_url(site):
        flash("Некорректный URL", "error")
        return redirect(url_for("get_index"))
    return "<h1>AAAAA</h1>"


# @app.route("/urls/<id>")
# def get_ulr_page(id):
#     return