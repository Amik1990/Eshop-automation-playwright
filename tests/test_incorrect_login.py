from pages import HomePage, LoginPage

def test_incorrect_login(load_home_page: HomePage, user_data):
    """
    Test ověří, že se nejde přihlásit s nevalidními daty uživatele.
    """
    # 1. Získání dat z fixtury
    email = user_data["email"]
    password = user_data["password"]

    # 2. Přejdeme na login stránku
    load_home_page.click_signup_login()

    # 3. Provedeme login s nevalidnimi daty
    login_page = LoginPage(load_home_page.page)
    login_page.expect_visible(login_page.loginToYourAccount, name="Login to your account")
    login_page.login_user(email, password)

    #4. Ověříme, že se zobrazila error hláška: Your email or password is incorrect!
    login_page.verify_incorrect_login()

    print("END OF TEST: INCORRECT LOGIN")


