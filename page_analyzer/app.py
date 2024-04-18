import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for

from page_analyzer.validator import get_url, validator
from page_analyzer.db import (get_id_url_from_base_urls,
                              get_all_urls_from_base_ulrs,
                              get_data_url_from_base_by_id,
                              write_data_to_base_urls)


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
connect = psycopg2.connect(DATABASE_URL)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


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
    url = get_url(site)
    errors = validator(url)
    if errors:
        for error in errors:
            flash(*error)
        return redirect(url_for("get_index", value=site))
    data = get_id_url_from_base_urls(connect, url)
    if data:
        flash("Страница уже существует", "success")
        id = data
    else:
        flash("Страница успешно добавлена", "success")
        id = write_data_to_base_urls(connect, url)
    return redirect(url_for("ulr_page", id=id), code=302)


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = get_all_urls_from_base_ulrs(connect)
    return render_template(
        "urls_page.html",
        urls=urls
    )



@app.route("/urls/<id>")
def ulr_page(id):
    id, site, created_at = get_data_url_from_base_by_id(connect, id)
    messages = get_flashed_messages(with_categories=True)
    return render_template("url_page.html",
                           messages=messages,
                           id=id,
                           site=site,
                           created_at=created_at.isoformat())