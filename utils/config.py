import os
from dotenv import load_dotenv
from pathlib import Path

# Načte proměnné ze souboru .env
# Cesta k .env souboru (o úroveň výš než utils)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """
    Třída pro načítání a poskytování konfiguračních proměnných.
    """
    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com/")
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", 5000))

# Vytvoření jedné instance, kterou bude používat celá aplikace
config = Config()