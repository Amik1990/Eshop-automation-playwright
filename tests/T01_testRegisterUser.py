from pages import HomePage, LoginPage

def test_register_user(load_home_page: HomePage):
    load_home_page.load()
