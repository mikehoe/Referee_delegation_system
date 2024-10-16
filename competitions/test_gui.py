from decouple import config
from selenium import webdriver
from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class GuiHomeTest(TestCase):

    def setUp(self):
        self.selenium_webdriver = webdriver.Chrome()
        self.wait = WebDriverWait(self.selenium_webdriver, 10)

    def test_home_page(self):
        self.selenium_webdriver.get('http://127.0.0.1:8000/')

        self.assertIn('Season 2024/2025', self.selenium_webdriver.page_source)

    def tearDown(self):
        self.selenium_webdriver.quit()


class GuiLoginTest(TestCase):

    def setUp(self):
        self.selenium_webdriver = webdriver.Chrome()
        self.wait = WebDriverWait(self.selenium_webdriver, 10)

    def test_login(self):
        self.selenium_webdriver.get('http://127.0.0.1:8000/accounts/login/')

        # Login with the data from .env
        username = config('SUPERUSER_USERNAME')
        password = config('SUPERUSER_PASSWORD')

        self.selenium_webdriver.find_element(By.ID, 'id_username').send_keys(username)
        self.selenium_webdriver.find_element(By.ID, 'id_password').send_keys(password)

        login_button = self.selenium_webdriver.find_element(By.XPATH, '//input[@value="Login"]')
        login_button.click()

        self.assertIn('Season 2024/2025', self.selenium_webdriver.page_source)

    def tearDown(self):
        self.selenium_webdriver.quit()