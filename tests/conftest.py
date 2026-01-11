import pytest
from faker import Faker
from utils.fixture_utils import setup_page
from pages import HomePage, LoginPage
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


