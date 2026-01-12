import re

from playwright.sync_api import expect

from .base_page import BasePage
from utils.config import config


class HomePage(BasePage):

    def load(self, url: str = f"{config.BASE_URL}") -> None:
        self.LOG.info(f"Načítám stránku {url}")
        self.navigate(url)
        self.accept_cookies()

        automationExercise = self.page.get_by_role("heading", name="AutomationExercise")
        self.expect_visible(automationExercise, name="Title Automation Exercise")
        self.LOG.info(f"Title Automation Exercise je viditelný.")

    def click_signup_login (self):
        signup_login_button = self.page.get_by_role("link", name=" Signup / Login")
        self.click(signup_login_button, name="Tlačítko Sign Up / Login")

        expect(self.page).to_have_url(re.compile("https://automationexercise.com/login"))
        self.LOG.info(f"Úspěšně přesměrováno na Login stránku.")



