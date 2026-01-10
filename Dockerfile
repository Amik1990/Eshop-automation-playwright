# Použijeme oficiální Playwright image s Pythonem
# Aktualizováno na verzi 1.57.0, aby odpovídala verzi knihovny v requirements.txt
FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Zkopírujeme seznam závislostí
COPY requirements.txt .

# Nainstalujeme Python knihovny
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme zbytek projektu do kontejneru
COPY . .

# Příkaz, který se spustí po startu kontejneru
# Spustíme testy a uložíme výsledky do složky /app/allure-results
CMD ["pytest", "--alluredir=allure-results"]