import json
import time

from playwright.sync_api import sync_playwright

from wttj_utils import EntrepriseInfo, goto, login, URL

def get_enterprises_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [EntrepriseInfo(name=ent['name'], link=ent['link']) for ent in data]

def apply_spontaneous(page, enterprise: EntrepriseInfo):
    with open('motivation_letter.txt', 'r') as file:
        motivation_letter = file.read().strip()

    path, params = enterprise.link.split('?')
    url = f"{URL}/companies/{path}/jobs?{params}"
    goto(page, url)
    button = page.locator('//div[.//span[text()="Candidature spontanée"]]//button[@data-testid="company_jobs-button-apply"]')
    if button.count() == 0:
        button = page.locator('//div[.//span[text()="Spontaneous application"]]//button[@data-testid="company_jobs-button-apply"]')
    if button.count() == 0:
        return
    button.click()


    time.sleep(1)
    textfield = page.locator('[data-testid="apply-form-field-cover_letter"]')
    if textfield.count() != 0:
        textfield.fill(motivation_letter)
    page.click('[data-testid="apply-form-terms"]')
    page.click('[data-testid="apply-form-consent"]')
    page.click('[data-testid="apply-form-submit"]')
    time.sleep(1)

def main():
    enterprises = get_enterprises_from_json('enterprises.json')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        goto(page, URL)
        login(page)

        for i, enterprise in enumerate(enterprises):
            apply_spontaneous(page, enterprise)
            print(f"Applied to {enterprise.name} ({i + 1}/{len(enterprises)})")


if __name__ == "__main__":
    main()