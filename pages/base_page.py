import re
from utils.exceptions import NetworkResponseError, ElementNotVisibleError
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

            # v try sekci pak pouziji vytvorenou funkci predicate
        try:
            with self.page.expect_response(predicate, timeout=10000):
                self.click(element, name)
            self.LOG.success(f"Odpověď pro {url_pattern} byla nalezena.")

        except Exception as e:
            self.LOG.error(f"Časový limit vypršel při čekání na odpověď '{url_pattern}' po kliknutí na '{name}'.")
            raise NetworkResponseError from e

    def expect_visible(self, element: Locator, name: str = "element", timeout: int = 5000) -> None:
        """
        Ověří, že je prvek viditelný.

        Args:
            element: Locator prvku.
            name: Název prvku pro logování.
            timeout: Maximální čas čekání v ms.
        """
        self.LOG.info(f"Ověřuji, zda {name} je viditelný.")
        try:
            expect(element).to_be_visible(timeout=timeout)
            self.LOG.success(f"Prvek '{name}' je viditelný")
        except Exception as e:
            self.LOG.error(f"Prvek '{name}' není viditelný! (Timeout: {timeout}ms)")
            # Vyhodíme naši vlastní chybu
            raise ElementNotVisibleError(name, timeout) from e

    def fill(self, selector: Locator | str, value: str, name: str = "input field") -> None:
        """
        Vyplnění input pole.
        Podporuje jak string selektor, tak Locator objekt.
        """
        # Pokud je v názvu pole "password" nebo "heslo", skryjeme hodnotu v logu
        log_value = "***" if any(s in name.lower() for s in ["password", "heslo"]) else value
        self.LOG.info(f"Vyplňování {name} s hodnotou: '{log_value}'")

        if hasattr(selector, "fill") and not isinstance(selector, str):
            selector.fill(value)
        else:
            self.page.fill(selector, value)

    def navigate(self, url:str) -> None:
        self.LOG.info(f"Navigace na URL: {url}")
        self.page.goto(url)
        # Změna z networkidle na load pro rychlejší a stabilnější načítání
        self.page.wait_for_load_state("load")

    def accept_cookies(self):
        """Pokusí se potvrdit cookies lištu, pokud je viditelná."""
        self.LOG.info(f"Kontrola přítomnosti cookies lišty")

        # 1. Specifická kontrola pro Google Funding Choices (častý overlay, který blokuje klikání)
        # Tlačítko pro souhlas má obvykle třídu .fc-cta-consent
        fc_consent_button = self.page.locator(".fc-cta-consent")
        if fc_consent_button.is_visible():
            self.click(fc_consent_button, "Google FC Consent Button")
            return

        # 2. Obecná kontrola pro ostatní lišty
        # Regex pro běžné texty: OK, Přijmout, Accept...
        # Používáme \b pro hranice slov, aby to nechytalo např. "Kookie" (obsahuje 'ok')
        pattern = re.compile(r"\b(OK|Přijmout|Accept|Souhlasím|Souhlas|Rozumím|Allow all)\b", re.IGNORECASE)

        # Hledáme tlačítko NEBO odkaz. .first vezme první nalezený
        button = self.page.get_by_role("button", name=pattern).or_(self.page.get_by_role("link", name=pattern)).first

        if button.is_visible():
            try:
                self.click(button, "Cookies Consent Button")
            except Exception as e:
                self.LOG.warning(f"Našel jsem tlačítko cookies, ale nešlo na něj kliknout: {e}")
        else:
            self.LOG.debug("Cookie lišta nebyla nalezena (nebo je již potvrzena).")
