from bs4 import BeautifulSoup


def html_parse(response):
    status_code = response.status_code
    soup = BeautifulSoup(response.text, "lxml")
    h1 = soup.find("h1").get_text()
    title = soup.find("head").find("title").get_text()
    description = soup.find("meta",
                            {"name": "description"}).get("content")
    return {"h1": h1,
            "status_code": status_code,
            "title": title,
            "description": description}
