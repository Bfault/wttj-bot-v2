import os
import time

URL = "https://www.welcometothejungle.com/fr"

class EntrepriseInfo:
    def __init__(self, name, link):
        self.name = name
        self.link = link

def get_wait_time():
    return 2

def goto(page, url):
    page.goto(url)
    time.sleep(get_wait_time())

def login(page):
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    time.sleep(get_wait_time())

    page.click('[data-testid="not-logged-visible-login-button"]')
    page.fill('[data-testid="login-field-email"]', email)
    page.fill('[data-testid="login-field-password"]', password)
    page.click('[data-testid="login-button-submit"]')
    time.sleep(get_wait_time())