import pytest
from faker import Faker
from utils.fixture_utils import setup_page
from pages import HomePage, LoginPage, SignupPage
from playwright.sync_api import Page
from utils.config import config

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Tato fixture nastavuje parametry pro spuštění prohlížeče.
    Hodnota headless se bere z konfigurace (.env).
    """
    return {
        **browser_type_launch_args,
        "headless": config.BROWSER_HEADLESS,  # Použití hodnoty z configu
        "slow_mo": 500,  # Volitelné: zpomalí test, abych viděl, co se děje
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Tato fixture umožní nastavit parametry pro prohlížeč.
    Pokud spustíš PWDEBUG=1, Playwright si headless mód pořeší sám.
    """
    return {
        **browser_context_args,
        "viewport": None,  # Nastavení velikosti okna
    }

@pytest.fixture()
def load_home_page(page: Page):
    return setup_page(HomePage, page)

@pytest.fixture()
def load_login_page(page: Page):
    return setup_page(LoginPage, page)

@pytest.fixture
def user_data():
    """Vygeneruje náhodná data pro uživatele."""
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "country": "United States", # Zde raději fixní hodnotu, aby seděla do select boxu
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.zipcode(),
        "mobile_number": fake.phone_number(),
        "company": fake.company(),
        "day": "15",
        "month": "9",
        "year": "2006"
    }


@pytest.fixture
def registered_user(page, user_data):
    """
    Tato fixtura provede registraci uživatele a vrátí jeho data.
    Používá se pro testy, které vyžadují existujícího uživatele (např. Login).
    """
    home_page = HomePage(page)
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # 1. Registrace
    home_page.load()
    home_page.click_signup_login()
    login_page.signup_user(user_data["name"], user_data["email"])

    #nasledujici radky muzu psat i bez promennych (červene): např: user_data["name"]
    signup_page.enter_account_information(
        name=user_data["name"],
        email=user_data["email"],
        password=user_data["password"],
        day=user_data["day"],
        month=user_data["month"],
        year=user_data["year"]
    )
    
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
    
    # Ověření, že jsme přihlášeni (po registraci nás to rovnou přihlásí)
    # home_page.verify_logged_in_user(user_data["name"]) # Toto může být v enter_address_information nebo zde

    # 2. Odhlášení (aby byl připraven čistý stav pro Login test)
    home_page.click_logout()

    # 3. Vrátíme data, aby test věděl, s kým se má přihlásit
    yield user_data

