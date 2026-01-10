import re

from utils.logger_config import get_logger
from playwright.sync_api import Page


class BasePage():
    def __init__(self, page: Page):
        self.page = page
        self.LOG = get_logger(self.__class__.__name__)

    def click(self, element, name: str = "element") -> None:
        """
              Kliknutí na element (podporuje string i Locator).

              Args:
                  element: Selektor (str) nebo Locator objekt.
                  name: Název prvku pro logování.
              """
        self.LOG.info(f"Kiknutí na {element}")
        # Zjišťujeme, zda je 'element' objekt Locator (má metodu .click()) nebo jen textový selektor (str).
        if hasattr(element, "click") and not isinstance(element, str):
            element.click()
        else:
            self.page.click(element)

    def navigate(self, url:str) -> None:
        self.LOG.info(f"Navigace na URL: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def accept_cookies(self):
        """Pokusí se potvrdit cookies lištu, pokud je viditelná."""
        self.LOG.info(f"Kontrola přítomnosti cookies lišty")
        # Regex pro běžné texty: OK, Přijmout, Accept, Souhlasím... (?i) = case insensitive
        pattern = re.compile(r"OK|Přijmout|Accept|Souhlasím|Rozumím|Allow all", re.IGNORECASE)

        # Hledáme tlačítko NEBO odkaz. .first vezme první nalezený, aby to nespadlo na 'strict mode'
        button = self.page.get_by_role("button", name=pattern).or_(self.page.get_by_role("link", name=pattern)).first

        if button.is_visible():
            self.click(button, "Cookies Consent Button")
        else:
            self.LOG.debug("Cookie lišta nebyla nalezena (nebo je již potvrzena).")
