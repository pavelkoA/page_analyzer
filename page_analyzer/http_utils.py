import requests


def check_url(url):
    response = requests.get(url=url)
    response.raise_for_status()
    return response.status_code
