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

    def new_user_signup_is_visible(self):
        new_user_signup_title = self.page.get_by_role("heading", name="New User Signup!")
        self.expect_visible(new_user_signup_title, name="New User Signup!")

    def signup_user(self, name: str, email: str):
        name_input = self.page.get_by_role("textbox", name="Name")
        email_input = self.page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address")
        signup_button = self.page.get_by_role("button", name="Signup")
        enter_account_information_heading = self.page.get_by_text("Enter Account Information")


        self.fill(name_input, name, name="Name input")
        self.fill(email_input, email, name="Email input")
        self.LOG.info(f"User {name} and email {email} is filled in.")
        self.click(signup_button, name="Signup button")
        self.expect_visible(enter_account_information_heading, name="Enter Account Information")




