from validators.url import url as url_validate
from urllib.parse import urlparse


def validatord(url):
    errors = []
    if not bool(url_validate(url)):
        errors.append(("Некорректный URL", "danger"))
    if len(url) > 255:
        errors.append(("Слишком длинный URL", "danger"))
    return errors


def normile_url(url):
    parse = urlparse(url)
    return parse.scheme + "://" + parse.hostname
