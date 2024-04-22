import os
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   get_flashed_messages,
                   url_for)

from page_analyzer.validator import get_url, validator
from page_analyzer.http_utils import check_url, url_parse
from page_analyzer.db_utils import (read_url_by_name,
                                    read_url_by_id,
                                    read_checks,
                                    read_urls_and_last_checks,
                                    write_url,
                                    write_url_checks,)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def get_index():
    value = request.args.get("value", default="")
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html",
                           messages=messages,
                           value=value)


@app.post("/urls")
def create_url():
    site = request.form.get("url")
    url = get_url(site)
    errors = validator(url)
    if errors:
        for error in errors:
            flash(*error)
        return redirect(url_for("get_index", value=site))
    data = read_url_by_name(url)
    if data:
        flash("Страница уже существует", "success")
    else:
        flash("Страница успешно добавлена", "success")
        write_url(url)
    data_id = read_url_by_name(url).id
    return redirect(url_for("ulr_page", id=data_id), code=302)


@app.get("/urls")
def get_urls():
    urls = read_urls_and_last_checks()
    return render_template(
        "urls_page.html",
        urls=urls
    )


@app.route("/urls/<id>")
def ulr_page(id):
    url_data = read_url_by_id(id)
    checks = read_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template("url_page.html",
                           messages=messages,
                           url_data=url_data,
                           checks=checks)


@app.post("/urls/<id>/checks")
def checks_url(id):
    url = read_url_by_id(id)
    try:
        status_code = check_url(url.name)
        h1, title, dedscription = url_parse(url.name)
        write_url_checks(id, status_code, h1, title, dedscription)
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("ulr_page", id=id), code=302)
