import os
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   get_flashed_messages,
                   url_for)

from page_analyzer.validator import get_url, validator
from page_analyzer.db_utils import (get_url_from_base_urls,
                                    get_all_urls_from_base_ulrs,
                                    get_url_from_base_urls_by_id,
                                    write_data_to_base_urls,
                                    get_checks_from_url_checks,
                                    write_new_check_from_url_checks)


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
    data = get_url_from_base_urls(url)
    if data:
        flash("Страница уже существует", "success")
        id = data.id
    else:
        flash("Страница успешно добавлена", "success")
        id = write_data_to_base_urls(url).id
    return redirect(url_for("ulr_page", id=id), code=302)


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = get_all_urls_from_base_ulrs()
    return render_template(
        "urls_page.html",
        urls=urls
    )


@app.route("/urls/<id>")
def ulr_page(id):
    url_data = get_url_from_base_urls_by_id(id)
    checks = get_checks_from_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template("url_page.html",
                           messages=messages,
                           url_data=url_data,
                           checks=checks)


@app.post("/urls/<id>/checks")
def checks_url(id):
    url_data = get_url_from_base_urls_by_id(id)
    write_new_check_from_url_checks(id, 200, "Hexlet",
                                    "title", "description")
    checks = get_checks_from_url_checks(id)
    return render_template("url_page.html",
                           url_data=url_data,
                           checks=checks)