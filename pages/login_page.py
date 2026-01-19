from .base_page import BasePage
from utils.config import config

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # --- LOKÁTORY ---
        self.loginToYourAccount = self.page.get_by_role("heading", name="Login to your account")
        
        # Signup lokátory
        self.name_input = self.page.get_by_role("textbox", name="Name")
        self.email_input = self.page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address")
        self.signup_button = self.page.get_by_role("button", name="Signup")
        self.enter_account_information_heading = self.page.get_by_text("Enter Account Information")
        
        # Login lokátory
        self.login_email_input = self.page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address")
        self.login_password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Login")


    def load(self, url: str = f"{config.BASE_URL}/login") -> None:
        self.LOG.info(f"Stránka {url} se načetla")
        self.navigate(url)
        self.accept_cookies()
        self.expect_visible(self.loginToYourAccount, name="Login to your account")
        self.LOG.info(f"Tile 'Login to your account' je viditelný.")

    def new_user_signup_is_visible(self):
        new_user_signup_title = self.page.get_by_role("heading", name="New User Signup!")
        self.expect_visible(new_user_signup_title, name="New User Signup!")

    def signup_user(self, name: str, email: str):
        self.fill(self.name_input, name, name="Name input")
        self.fill(self.email_input, email, name="Email input")
        self.LOG.info(f"User {name} and email {email} is filled in.")
        self.click(self.signup_button, name="Signup button")
        self.expect_visible(self.enter_account_information_heading, name="Enter Account Information")

    def login_user(self, email: str, password: str):
        """Přihlášení uživatele."""
        self.LOG.info(f"Přihlašuji uživatele: {email}")
        self.fill(self.login_email_input, email, name="Login Email")
        self.fill(self.login_password_input, password, name="Login Password")
        self.click(self.login_button, name="Login Button")
