from pages import HomePage, LoginPage, SignupPage
import pytest

# Parametrize necháme jen pro datum narození (pokud ho chceme měnit)
@pytest.mark.parametrize(
    "day, month, year", 
    [("15", "9", "2006")]
)
def test_register_user(load_home_page: HomePage, user_data, day, month, year):
    # Rozbalíme data z fixtury user_data
    name = user_data["name"]
    email = user_data["email"]
    password = user_data["password"]
    # Akce
    load_home_page.click_signup_login()
    login_page = LoginPage(load_home_page.page)
    login_page.new_user_signup_is_visible()
    login_page.signup_user(name, email)
    signup_page = SignupPage(login_page.page)
    signup_page.enter_account_information(name, email, password, day, month, year)
    signup_page.enter_address_information(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        company=user_data["company"],
        address=user_data["address"],
        country=user_data["country"],
        state=user_data["state"],
        city=user_data["city"],
        zipcode=user_data["zipcode"],
        mobile_number=user_data["mobile_number"]
    )
    home_page = HomePage(signup_page.page)
    home_page.verify_logged_in_user(name)
    home_page.delete_account()
    home_page.click_continue()
    print("END OF TEST: REGISTER USER")

