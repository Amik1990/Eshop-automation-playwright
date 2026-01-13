from pages import HomePage, LoginPage
import pytest

@pytest.mark.parametrize(
    "name, email", [("Daniel J","zubnicentrum@gmail.com")]
)
def test_register_user(load_home_page: HomePage, name, email):
    load_home_page.click_signup_login()
    login_page = LoginPage(load_home_page.page)
    login_page.new_user_signup_is_visible()
    login_page.signup_user(name, email)







