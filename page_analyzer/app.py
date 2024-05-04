import os
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for)

from page_analyzer.validator import get_url, validator
from page_analyzer.http_utils import url_parse
from page_analyzer import db


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    value = request.args.get("value", default="")
    return render_template("index.html",
                           value=value)


@app.post("/urls")
def create_url():
    site = request.form.get("url")
    errors = validator(site)
    if errors:
        for error in errors:
            flash(*error)
        return render_template("index.html",
                               value=site), 422
    url = get_url(site)
    data = db.get_url(url)
    if data:
        flash("Страница уже существует", "success")
    else:
        flash("Страница успешно добавлена", "success")
        db.write_url(url)
    data_id = db.get_url(url).id
    return redirect(url_for("show_url_page", id=data_id))


@app.get("/urls")
def get_urls():
    urls = db.read_urls_and_last_checks()
    return render_template(
        "urls/list.html",
        urls=urls
    )


@app.route("/urls/<int:id>")
def show_url_page(id):
    url_data = db.get_url(id)
    checks = db.read_checks(id)
    return render_template("urls/detail.html",
                           url_data=url_data,
                           checks=checks)


@app.post("/urls/<int:id>/checks")
def check_url(id):
    url = db.get_url(id)
    try:
        url_data = url_parse(url.name)
        url_data["url_id"] = id
        db.write_url_checks(url_data)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("show_url_page", id=id))
