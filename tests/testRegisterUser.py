from pages import HomePage, LoginPage
from pages import base_page

def test_register_user(load_home_page: HomePage):
    load_home_page.load()
    load_home_page.click_signup_login()





