import re
from playwright.sync_api import expect
from .base_page import BasePage
from utils.config import config


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # --- LOKÁTORY ---
        self.automationExercise = self.page.get_by_role("heading", name="AutomationExercise")
        self.signup_login_button = self.page.get_by_role("link", name=" Signup / Login")
        self.delete_account_button = self.page.get_by_role("link", name=" Delete Account")
        self.account_deleted_title = self.page.get_by_text("Account Deleted!")
        self.continue_button = self.page.get_by_role("link", name="Continue")

    def load(self, url: str = f"{config.BASE_URL}") -> None:
        self.LOG.info(f"Načítám stránku {url}")
        self.navigate(url)
        self.accept_cookies()
        self.expect_visible(self.automationExercise, name="Title Automation Exercise")
        self.LOG.info(f"Title Automation Exercise je viditelný.")

    def click_signup_login (self):
        self.click(self.signup_login_button, name="Tlačítko Sign Up / Login")
        expect(self.page).to_have_url(re.compile("https://automationexercise.com/login"))
        self.LOG.info(f"Úspěšně přesměrováno na Login stránku.")

    def verify_logged_in_user(self, name: str):
        username = self.page.get_by_text(f"Logged in as {name}")
        self.expect_visible(username, name=f"Logged in as {name}")

    def delete_account(self):
        self.click(self.delete_account_button, name=" Delete Account")
        self.expect_visible(self.account_deleted_title, name="Account Deleted!")

    def click_continue(self):
        self.click(self.continue_button, name="Continue")
        expect(self.page).to_have_url(re.compile("https://automationexercise.com"))
        self.LOG.info(f"Úspěšně přesměrováno na Home page.")







