from playwright.sync_api import Page
from utils.logger_config import get_logger

# Zde si ručně pojmenuju logger jako "FixtureUtils".
# Protože toto není třída (class), nemůžeme použít self.__class__.__name__.
# Díky tomu v logu uvidíme: [INFO] [FixtureUtils] ... zpráva ...
LOG = get_logger("FixtureUtils")

def setup_page (PageClass, page: Page):
    class_name = PageClass.__name__
    LOG.info(f"---SETUP: inicializace {class_name}---")

    try:
        instance = PageClass(page)
        instance.load()
        LOG.success(f"FIXTURE: {class_name} připravena.")
        return instance

    except Exception as e:
        LOG.error(f"SELHÁNÍ SETUPU: stránka {class_name} se nenačetla.")
        LOG.error(f"Detail: {str(e)}")

        # Automatický screenshot při selhání jakékoliv fixtury
        screenshot_path = f"screenshots/setup_fail_{class_name}.png"
        page.screenshot(path=screenshot_path)

        raise e # Vyhození chyby dál