from pages import HomePage, LoginPage, SignupPage
import pytest

@pytest.mark.parametrize(
    "name, email, password, day, month, year, first_name, last_name, company, address, country, state, city, zipcode, mobile_number",
    [("Daniel J", "zubnicentrum@gmail.com", "Blbec2", "15", "9", "2006", "Daniel", "Connor", "KBC", "Skacelova", "United States", "Morava", "Brno", "62100", "735666985")]
)
def test_register_user(load_home_page: HomePage, name, email, password, day, month, year, first_name, last_name, company, address, country, state, city, zipcode, mobile_number):
    load_home_page.click_signup_login()
    login_page = LoginPage(load_home_page.page)
    login_page.new_user_signup_is_visible()
    login_page.signup_user(name, email)
    signup_page = SignupPage(login_page.page)
    signup_page.enter_account_information(name, email, password, day, month, year)
    signup_page.enter_address_information(first_name, last_name, company, address, country, state, city, zipcode, mobile_number)
