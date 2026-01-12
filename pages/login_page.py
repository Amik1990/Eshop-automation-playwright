from .base_page import BasePage
from utils.config import config

class LoginPage(BasePage):

    def load(self, url: str = f"{config.BASE_URL}/login") -> None:
        self.LOG.info(f"Stránka {url} se načetla")
        self.navigate(url)
        self.accept_cookies()

        loginToYourAccount = self.page.get_by_role("heading", name="Login to your account")
        self.expect_visible(loginToYourAccount, name="Login to your account")
        self.LOG.info(f"Tile 'Login to your account' je viditelný.")

