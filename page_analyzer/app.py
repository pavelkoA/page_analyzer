import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for

from page_analyzer.validator import get_url, is_url


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
connect = psycopg2.connect(DATABASE_URL)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_data_in_base_urls(connect, data):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT *
                FROM urls
                WHERE name = '{data}'"""
        )
        return cursor.fetchone()

def get_data_in_base_id(connect, id):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT *
                FROM urls
                WHERE id = '{id}'"""
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
            connect.commit()
            return get_data_in_base_urls(connect, data)
        return base_data


def get_all_urls_in_base(connect):
    with connect.cursor() as cursor:
        cursor.execute("""SELECT *
                          FROM urls
                          ORDER BY id DESC""")
        return cursor.fetchall()

@app.route("/")
def get_index():
    value = request.args.get("value", default="")
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html",
                           messages=messages,
                           value=value)


@app.route("/urls", methods=['POST'])
def create_url():
    site = request.form.get("url")
    if not is_url(site):
        flash("Некорректный URL", "error")
        return redirect(url_for("get_index", value=site))
    data = get_data_in_base_urls(connect, get_url(site))
    if data:
        flash("Страница уже существует", "success")
        id, *other_data = data
    else:
        flash("Страница успешно добавлена", "success")
        id, *other_data = write_data_to_base_urls(connect, get_url(site))
    return redirect(url_for("ulr_page", id=id), code=302)


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = get_all_urls_in_base(connect)
    return render_template(
        "urls_page.html",
        urls=urls
    )



@app.route("/urls/<id>")
def ulr_page(id):
    id, site, created_at = get_data_in_base_id(connect, id)
    messages = get_flashed_messages(with_categories=True)
    return render_template("url_page.html",
                           messages=messages,
                           id=id,
                           site=site,
                           created_at=created_at.isoformat())