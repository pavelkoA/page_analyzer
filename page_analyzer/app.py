import os
import requests
from fake_useragent import UserAgent
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for)
from werkzeug.exceptions import HTTPException

from page_analyzer.utilits import normalize_url, validate
from page_analyzer.html_parser import html_parse
from page_analyzer import db
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


DATABASE_URL = os.getenv("DATABASE_URL")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def create_url():
    with db.connect_db(DATABASE_URL) as connect_db:
        input_url = request.form.get("url")
        errors = validate(input_url)
        if errors:
            for error in errors:
                flash(*error)
            return render_template("index.html",
                                   value=input_url), 422
        normile_url = normalize_url(input_url)
        data = db.get_url(connect_db, normile_url)
        if data:
            flash("Страница уже существует", "success")
        else:
            flash("Страница успешно добавлена", "success")
            db.write_url(connect_db, normile_url)
        data_id = db.get_url(connect_db, normile_url).id
        return redirect(url_for("show_url_page", id=data_id))


@app.get("/urls")
def get_urls():
    with db.connect_db(DATABASE_URL) as connect_db:
        urls = db.read_urls_and_last_checks(connect_db)
        return render_template(
            "urls/list.html",
            urls=urls
        )


@app.route("/urls/<int:id>")
def show_url_page(id):
    with db.connect_db(DATABASE_URL) as connect_db:
        url_data = db.get_url(connect_db, id)
        checks = db.read_checks(connect_db, id)
        return render_template("urls/detail.html",
                               url_data=url_data,
                               checks=checks)


@app.post("/urls/<int:id>/checks")
def check_url(id):
    with db.connect_db(DATABASE_URL) as connect_db:
        url = db.get_url(connect_db, id).name
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        try:
            response = requests.get(url=url,
                                    headers=headers,
                                    timeout=5)
            response.raise_for_status()
            url_data = html_parse(response)
            url_data["url_id"] = id
            db.write_url_checks(connect_db, url_data)
            flash("Страница успешно проверена", "success")

        except Exception as ex:
            print(ex)
            flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url_page", id=id))


@app.errorhandler(HTTPException)
def page_not_found(e):
    return render_template("errors/404.html",
                            error=e), e.code


@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500
