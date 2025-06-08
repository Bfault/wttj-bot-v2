import json
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from wttj_utils import EntrepriseInfo, get_wait_time, goto, login, URL

def get_enterprises_info(page, query: str, blacklist: list = None):
    if blacklist is None:
        blacklist = []

    def get_last_page(page, query):
        url = f"{URL}/companies?query={query}&page=1"
        goto(page, url)
        page.get_by_label("Candidatures spontanées acceptées").click()
        time.sleep(get_wait_time())
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        pagination_items = soup.select('[data-testid="companies-search-pagination"] li')
        if len(pagination_items) < 2:
            return 1
        last_page = int(pagination_items[-2].get_text(strip=True))
        return last_page

    last_page = get_last_page(page, query)
    enterprises = []

    for page_num in range(1, last_page+1):
        if last_page > 1:
            page.locator(f'//nav[@aria-label="Pagination"]//a[normalize-space(text())="{page_num}"]').click()
            time.sleep(get_wait_time())

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        companies = soup.select('[data-testid="companies-search-search-results"] li')
        for company in companies:
            article = company.find('article', {'data-testid': 'company-card'})
            if not article:
                continue
            name = article.find('img')['alt'].strip()
            link = article.find('a')['href'].strip()
            link = link.split('/')[-1]
            if name.lower() in blacklist:
                continue
            enterprises.append(EntrepriseInfo(name, link))
        

    return enterprises

def main(save=False):
    queries = ["backend", "devops", "mlops", "data"]
    blacklist = ["alyce", "milvue"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        goto(page, URL)
        login(page)
        
        enterprises: EntrepriseInfo = []
        for query in queries:
            enterprises += get_enterprises_info(page, query, blacklist)

        unique_enterprises = {e.name.lower(): e for e in enterprises}.values()
        for enterprise in unique_enterprises:
            print(f"Name: {enterprise.name}, Link: {URL}/companies/{enterprise.link}")
        if save:
            with open('enterprises.json', 'w') as f:
                json.dump([e.__dict__ for e in unique_enterprises], f, indent=4)

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main(save=True)