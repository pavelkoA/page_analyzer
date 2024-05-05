import pytest
from playwright.sync_api import Playwright, expect


test_data = [("https://ru.hexlet.ru", 1),
             ("https://ya.ru", 2),
             ("https://ya.ru", 2)]


def add_url_analyzer(page, url):
    page.goto("http://127.0.0.1:8001")
    page.locator("input[name='url']").fill(url)
    page.locator("input[type='submit']").click()
    page.goto("http://127.0.0.1:8001/urls")
    return page.locator("tbody").locator("tr")


@pytest.mark.parametrize("url, counter", test_data)
def test_index_page(playwright: Playwright, url, counter) -> None:
    browser = playwright.chromium.launch(headless=True)
    contex = browser.new_context()
    page = contex.new_page()

    item = add_url_analyzer(page, url)
    expect(item).to_have_count(counter)

    item2 = add_url_analyzer(page, url)
    expect(item2).to_have_count(counter)

    item3 = add_url_analyzer(page, url)
    expect(item3).to_have_count(counter)
