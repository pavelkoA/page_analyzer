from validators.url import url as url_validate
from urllib.parse import urlparse


def validate(input_url):
    errors = []
    if not input_url:
        errors.append(("URL обязателен для заполнения", "danger"))
    if not bool(url_validate(input_url)):
        errors.append(("Некорректный URL", "danger"))
    if len(input_url) > 255:
        errors.append(("Слишком длинный URL", "danger"))
    return errors


def normalize_url(input_url):
    url_data = urlparse(input_url)
    return url_data.scheme + "://" + url_data.hostname
