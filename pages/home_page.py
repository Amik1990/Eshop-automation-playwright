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
