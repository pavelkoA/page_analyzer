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
from page_analyzer.db_utils import (read_url,
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
    errors = validator(site)
    if errors:
        for error in errors:
            flash(*error)
        messages = get_flashed_messages(with_categories=True)
        return render_template("index.html",
                               messages=messages,
                               value=site), 422
    url = get_url(site)
    data = read_url(url)
    if data:
        flash("Страница уже существует", "success")
    else:
        flash("Страница успешно добавлена", "success")
        write_url(url)
    data_id = read_url(url).id
    return redirect(url_for("ulr_page", id=data_id))


@app.get("/urls")
def get_urls():
    urls = read_urls_and_last_checks()
    return render_template(
        "urls_page.html",
        urls=urls
    )


@app.route("/urls/<int:id>")
def ulr_page(id):
    url_data = read_url(id)
    checks = read_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template("url_page.html",
                           messages=messages,
                           url_data=url_data,
                           checks=checks)


@app.post("/urls/<int:id>/checks")
def checks_url(id):
    url = read_url(id)
    try:
        url_data = url_parse(url.name)
        url_data["status_code"] = check_url(url.name)
        url_data["url_id"] = id
        write_url_checks(url_data)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("ulr_page", id=id))
