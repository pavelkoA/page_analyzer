import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent()
headers = {'User-Agent': ua.random}


def check_url(url):
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    return response.status_code


def url_parse(url):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    h1 = soup.find("h1").get_text()
    title = soup.find("head").find("title").get_text()
    description = soup.find("meta",
                            {"name": "description"}).get("content")
    return h1, title, description
