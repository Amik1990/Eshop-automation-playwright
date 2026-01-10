import re

from utils.logger_config import get_logger
from playwright.sync_api import Page, Locator, expect, Response


class BasePage():
    def __init__(self, page: Page):
        self.page = page
        self.LOG = get_logger(self.__class__.__name__)


    # name: str = "element" znamená, že parametr je nepovinný.
    # Pokud při volání funkce nezadáme název, použije se automaticky text "element".
    # Slouží to hlavně pro hezčí výpis v logu (např. "Kliknutí na Tlačítko Odeslat" vs "Kliknutí na element").
    def click(self, element, name: str = "element") -> None:
        """
              Kliknutí na element (podporuje string i Locator).

              Args:
                  element: Selektor (str) nebo Locator objekt.
                  name: Název prvku pro logování.
              """
        self.LOG.info(f"Kiknutí na {name}")
        # Zjišťujeme, zda je 'element' objekt Locator (má metodu .click()) nebo jen textový selektor (str).
        if hasattr(element, "click") and not isinstance(element, str):
            element.click()
        else:
            self.page.click(element)


    def click_and_wait_for_response(self, element: Locator | str, url_pattern: str, name: str = "element") -> None:
        self.LOG.info(f"Klikám na {name} a čekám na odpověd obsahující {url_pattern}.")

        def predicate(response: Response):
            # Zde kontrolujeme, zda je to ta URL, na kterou čekáme.
            # 1. re.search(...): Zkusíme to najít jako Regex (pro složité vzory jako r"(?i)basket").
            # 2. or (... in ...): Pojistka - zkusíme to najít jako obyčejný text.
            url_match = re.search(url_pattern, response.url) or (url_pattern in response.url)
            # Vracíme True (našli jsme) jen pokud sedí URL A ZÁROVEŇ server řekl "200 OK".
            return url_match and response.status == 200

        pokracovat

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
