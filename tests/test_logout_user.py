from pages import HomePage, LoginPage

def test_logout_user(load_home_page: HomePage, registered_user):
    """
    Test ověří odhlášení existujícího uživatele.
    Uživatel je vytvořen fixturou 'registered_user'.
    """
    # 1. Získání dat z fixtury
    email = registered_user["email"]
    password = registered_user["password"]
    name = registered_user["name"]

    # 2. Přejdeme na login stránku
    load_home_page.click_signup_login()

    # 3. Provedeme login
    login_page = LoginPage(load_home_page.page)
    login_page.expect_visible(login_page.loginToYourAccount, name="Login to your account")
    login_page.login_user(email, password)

    #4. Ověříme, že jsme přihlášeni
    load_home_page.verify_logged_in_user(name)

    # 5. Odhlášení účtu
    load_home_page.click_logout()
    print("END OF TEST: LOGOUT USER")


