import sys                                  # Import modulu pro standardní vstup/výstup
from loguru import logger                   # Import pokročilé logovací knihovny
from pathlib import Path                    # Import pro práci s cestami

# --- Zjištění kořenové složky a příprava cesty pro logy ---
# Předpokládáme strukturu: D:/projekt/utils/logger_config.py
# .parent = utils, .parent.parent = D:/projekt
ROOT_DIR = Path(__file__).parent.parent
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE_PATH = LOG_DIR / "test_execution.log"

# Vytvoření složky logs, pokud neexistuje
LOG_DIR.mkdir(exist_ok=True)


# --- Konfigurace Logování ---

logger.remove()                             # Odstranění defaultní konfigurace loggeru

# Přidání konfigurace pro logování do konzole (stderr)
logger.add(
    sys.stderr,                             # Cíl: Standardní chybový výstup (terminál)
    level="INFO",                           # Logovací úroveň pro konzoli (zobrazuje se INFO a vyšší)
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>", # Formát s barvami
    colorize=True                           # Zapnutí barevného výstupu
)

# Přidání konfigurace pro logování do souboru (pro detailní audit)
logger.add(
    LOG_FILE_PATH,                          # Absolutní cesta k souboru v složce logs
    level="DEBUG",                          # Logovací úroveň pro soubor (nejnižší, zaznamená vše)
    mode="w",                               # "w" = Write (přepsat soubor při každém startu). Default je "a" (append).
    rotation="5 MB",                        # Soubor se otočí po 5 MB (pokud by jeden test vygeneroval tolik dat)
    compression="zip",                      # Staré soubory budou zkomprimovány
    enqueue=True,                           # Zajistí thread-safe logování, důležité pro paralelní testy
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
)

def get_logger(name):
    """Vrátí logger s kontextovým jménem (např. název třídy/modulu)."""
    return logger.bind(name=name)           # Používá bind pro přidání kontextové proměnné 'name'