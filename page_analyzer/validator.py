from validators.url import url as url_validate
from urllib.parse import urlparse


def is_url(url):
    return bool(url_validate(url))

def get_url(url):
    parse = urlparse(url)
    return parse.scheme + "://" + parse.hostname
